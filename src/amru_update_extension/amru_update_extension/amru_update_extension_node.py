"""PlayAudio: play the team's pre-recorded clips (Urdu, Mandarin, Malay) from the audio/ folder."""
import os
import shutil
import subprocess

from ament_index_python.packages import get_package_share_directory
from bt_common.executor_node import ExtensionExecutor, PortError, port_bool, port_str, run_executor


def audio_dir():
    return os.path.join(get_package_share_directory('amru_update_extension'), 'audio')


def resolve_clip(name, folder):
    """A bare file name only (no folders), and it must exist in the audio folder."""
    name = (name or '').strip()
    if not name or os.path.basename(name) != name or name.startswith('.'):
        raise PortError(f'file must be a clip name from the audio folder, got {name!r}')
    path = os.path.join(folder, name)
    if not os.path.isfile(path):
        raise PortError(f'unknown clip {name!r}; available: {", ".join(sorted(os.listdir(folder)))}')
    return path


def player_cmd(path):
    ffplay = shutil.which('ffplay')
    if not ffplay:
        raise PortError('ffplay not found (sudo apt install ffmpeg)')
    return [ffplay, '-nodisp', '-autoexit', '-loglevel', 'quiet', path]


class AmruUpdateExtension(ExtensionExecutor):
    def __init__(self):
        super().__init__('amru_update_extension')
        self.declare_parameter('audio_dir', '')        # '' = share/amru_update_extension/audio
        self.declare_parameter('max_clip_sec', 60.0)
        self.folder = self.get_parameter('audio_dir').value or audio_dir()
        self.handlers = {'PlayAudio': self._play}
        self.get_logger().info(f'{len(os.listdir(self.folder))} clips in {self.folder}')

    def _play(self, ports, ctl):
        path = resolve_clip(port_str(ports, 'file'), self.folder)
        proc = subprocess.Popen(player_cmd(path), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not port_bool(ports, 'wait', True):
            return True, f'playing {os.path.basename(path)}'
        waited, limit = 0.0, self.get_parameter('max_clip_sec').value
        while proc.poll() is None:
            if ctl.cancelled or waited > limit:
                proc.terminate()
                return False, 'cancelled' if ctl.cancelled else 'clip too long'
            ctl.sleep(0.1)
            waited += 0.1
        if proc.returncode != 0:
            return False, f'player exited with code {proc.returncode}'
        return True, f'played {os.path.basename(path)}'


def main():
    run_executor(AmruUpdateExtension)
