import argparse
import os, pwd
import stat
from pathlib import Path

parser = argparse.ArgumentParser();
parser.add_argument("f_name");
parser.add_argument("bin_p");
parser.add_argument("dsk_p");

def home_dir()->Path:
    sudo = os.environ.get("SUDO_USER");
    if sudo:
        return Path(pwd.getpwnam(sudo).pw_dir);
    return Path.home();

class GetPath:
    def __init__(self)->None:
        home:Path = home_dir();
        self.bin_path: Path = Path("/usr/local/bin");
        self.dsk_path: Path = home / ".local" / "share" / "applications";

class Input:
    def __init__(self, args:argparse.Namespace)->None:
        self.bin_abs: Path = Path(args.bin_p).resolve();
        self.dsk_abs: Path = Path(args.dsk_p).resolve();
        self.f_name: Path = Path(args.f_name);

class TargetPath:
    def __init__(self, gp:GetPath, ui:Input)->None:
        self.tgt_bin_path:Path = gp.bin_path / f"d4l_{ui.bin_abs.name}";
        self.tgt_dsk_path:Path = gp.dsk_path / f"d4l_{ui.dsk_abs.name}.desktop";

def make_symlink(src:Path, dst:Path)->None:
    dst.parent.mkdir(parents=True, exist_ok=True);
    if dst.is_symlink() or dst.exists():
        dst.unlink();
    os.symlink(src, dst);

def main() -> None:
    args = parser.parse_args();
    gp = GetPath();
    ui = Input(args);
    tgt = TargetPath(gp, ui);

    make_symlink(ui.bin_abs, tgt.tgt_bin_path);
    print(f"Symlink created: {tgt.tgt_bin_path} -> {os.readlink(tgt.tgt_bin_path)}");
    print(f"ICON PATH {str(tgt.tgt_dsk_path)}");

    with open(tgt.tgt_dsk_path, "w") as f:
        f.write("[Desktop Entry]\n"
            f"Name={ui.f_name}\n"
            f"Exec={tgt.tgt_bin_path}\n"
            f"Terminal=false\n"
            f"Type=Application\n"
            f"Icon={tgt.tgt_dsk_path}\n"
            f"StartupWMClass={ui.f_name}\n"
            f"Comment={ui.f_name}\n"
            f"Categories=Utility;\n");
        f.close();

    st = os.stat(tgt.tgt_bin_path);
    os.chmod(tgt.tgt_bin_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXUSR);
if __name__ == "__main__":
    main();
