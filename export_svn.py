import celery
import pysvn
import tempfile


@celery.task()
def export_svn(repo, rev):
    svn_client = pysvn.Client()
    tmp_dir = tempfile.mkdtemp()
    rev = pysvn.Revision(pysvn.opt_revision_kind.number, rev)
    svn_client.export(repo, tmp_dir, revision=rev, force=True)
    return tmp_dir
