import os, pwd
import stat
import sys
from os import unlink
from pathlib import Path

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
    def __init__(self)->None:
        self.bin_abs: Path = Path(sys.argv[1]).resolve();
        self.dsk_abs: Path = Path(sys.argv[2]).resolve();
        self.f_name: Path = Path(sys.argv[3]);

class TargetPath:
    def __init__(self, gp:GetPath)->None:

        if sys.argv[1] == "rm":
            self.tgt_bin_path: Path = gp.bin_path / f"d4l_{sys.argv[2]}";
            self.tgt_dsk_path:Path = gp.dsk_path / f"d4l_{sys.argv[2]}_icon.desktop";
            return

        self.tgt_bin_path:Path = gp.bin_path / f"d4l_{sys.argv[3]}";
        self.tgt_dsk_path:Path = gp.dsk_path / f"d4l_{sys.argv[3]}_icon.desktop";

def make_symlink(src:Path, dst:Path)->None:
    dst.parent.mkdir(parents=True, exist_ok=True);
    if dst.is_symlink() or dst.exists():
        dst.unlink();
    os.symlink(src, dst);

def remove_files() -> None:
    if sys.argv[1] == "rm":
        gp = GetPath();
        tgt = TargetPath(gp);

        unlink(tgt.tgt_bin_path);
        unlink(tgt.tgt_dsk_path);

def main() -> None:

    if len(sys.argv) <= 2 or len(sys.argv) > 4:
        print("\nusage:\n'desktop <executable file> <icon> <name>' to create a shortcut \n or \n'desktop rm <name>' to remove the shortcut \n");
        return;

    if sys.argv[1] == "rm" and len(sys.argv) == 3 :
        remove_files();
        print(f"Shortcut for {sys.argv[2]} Removed");
        return;

    elif sys.argv[1] == "rm" and len(sys.argv) != 3:
        print("\nusage:\n'desktop <executable file> <icon> <name>' to create a shortcut \n or \n'desktop rm <name>' to remove the shortcut \n");
        return;

    gp = GetPath();
    ui = Input();
    tgt = TargetPath(gp);

    make_symlink(ui.bin_abs, tgt.tgt_bin_path);
    print(f"Symlink created: {tgt.tgt_bin_path} -> {os.readlink(tgt.tgt_bin_path)}");
    print("Shortcut created\n");

    with open(tgt.tgt_dsk_path, "w") as f:
        f.write("[Desktop Entry]\n"
            f"Name={ui.f_name}\n"
            f"Exec={tgt.tgt_bin_path}\n"
            f"Terminal=false\n"
            f"Type=Application\n"
            f"Icon={ui.dsk_abs}\n"
            f"StartupWMClass={ui.f_name}\n"
            f"Comment={ui.f_name}\n"
            f"Categories=Utility;\n");
        f.close();

    st = os.stat(tgt.tgt_bin_path);
    os.chmod(tgt.tgt_bin_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXUSR);

if __name__ == "__main__":
    main();