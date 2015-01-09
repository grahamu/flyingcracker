import fc3 as project

VERSION = (0, 2, None)

def get_version():
    "Returns the version as a human-format string."
    v = '.'.join([str(i) for i in VERSION[:-1]])
    
    try:
        from mercurial import ui,hg
        from mercurial.node import hex
    except ImportError:
        svn = "HG-not-imported"
    else:
        project_path = project.__path__[0]
        try:
            repo = hg.repository(ui.ui(), project_path)
        except RepoError:
            svn = "HG-repo-not-found"
        else:
            fctx = repo.filectx(project_path, 'tip')
            svn = "HG-%s-%s" % (fctx.branch(), fctx.hex()[0:12])
    
    if VERSION[-1]:
        v = '%s-%s-%s' % (v, VERSION[-1], svn)
    else:
        v = '%s-%s' % (v, svn)
    return v
