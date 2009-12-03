import os
join = os.path.join

class ZEOInstanceBuilder:
    
    def create(self, location, *args):
        os.mkdir(location)
        for sub in ('etc', 'bin'):
            os.mkdir(join(location, sub))
        content = 'PYTHONPATH="$ZODB3_HOME"'
        bin_dir = join(location, 'bin')
        for script in ('runzeo', 'zeoctl'):
            f = open(join(bin_dir, script), 'w')
            f.write(content)
            f.close()

