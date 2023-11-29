with open("input.txt", "r") as f:
    lines = f.readlines()


class FSEntry:
    def __init__(self, name: str, size: int, parent: "Dir"):
        self.name, self.size, self.parent = name, size, parent


class Dir(FSEntry):
    def __init__(self, name: str, parent: "Dir"):
        super().__init__(name, 0, parent)
        self.children: list[FSEntry] = []

    def __str__(self):
        return f"{self.name}: {self.size}"

    def print(self, indent=0):
        print(f"{' '*indent}- {self.name} (dir, size={self.size})")
        indent += 2
        for c in self.children:
            c.print(indent)

    def get_or_add_child(self, name, makechild):
        child = next((d for d in self.children if d.name == name), None)
        if not child:
            child = makechild()
            self.children.append(child)
        return child

    def calc_size(self):
        self.size = 0
        for c in self.children:
            if isinstance(c, File):
                self.size += c.size
            else:
                self.size += c.calc_size()
        return self.size

    def flatten(self):
        yield self
        for c in self.children:
            if isinstance(c, Dir):
                yield from c.flatten()


class File(FSEntry):
    def __init__(self, name, size, parent: Dir):
        super().__init__(name, size, parent)

    def print(self, indent=0):
        print(f"{' '*indent}- {self.name} (file, size={self.size})")


root = Dir("/", None)
cwd = root
i = 0


while True and i < len(lines):
    _, cmd, *args = lines[i].split()
    if cmd == "cd":
        if args[0] == "/":
            cwd = root
        elif args[0] == "..":
            cwd = cwd.parent
        else:
            cwd = cwd.get_or_add_child(args[0], lambda: Dir(args[0], cwd))

        i += 1
    elif cmd == "ls":
        i += 1
        while i < len(lines) and lines[i][0] != "$":
            size, name = lines[i].split()
            if size == "dir":
                cwd.get_or_add_child(name, lambda: Dir(name, cwd))
            else:
                cwd.get_or_add_child(name, lambda: File(name, int(size), cwd))
            i += 1

root.calc_size()
# root.print()


def part1():
    size = sum(d.size for d in root.flatten() if d.size <= 100000)
    print(size)


def part2():
    free = 70_000_000 - root.size
    todelete = 30_000_000 - free
    dirs = list(sorted(root.flatten(), key=lambda dir: dir.size))
    for d in dirs:
        if d.size >= todelete:
            print(d)
            break


# part1()
part2()
