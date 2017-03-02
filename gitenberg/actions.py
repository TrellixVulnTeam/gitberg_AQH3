# these methods with signature: action(repo, *args, **kwargs)
# can be applied to a repo 

from github3 import login
from github3.exceptions import UnprocessableEntity
from .book import Book
from .make import NewFilesHandler
from .parameters import GITHUB_ORG as orgname
from .util.catalog import get_repo_name

def get_id(repo):
    book = Book(None, repo_name=repo)

    repo = book.github_repo.github.repository(orgname, repo)
    print repo.id
    return repo.id
    
def delete(repo_name):
    repo_name = get_repo_name(repo_name)
    book = Book(None, repo_name=repo_name)

    repo = book.github_repo.github.repository(orgname, repo_name)
    if repo:
        if repo.delete():
            print "{} deleted".format(repo_name)
        else:
            print "couldn't delete {}".format(repo_name)
    else:
        print "{} didn't exist".format(repo_name)
        
def add_generated_cover(repo_name, tag=False):
    repo_name = get_repo_name(repo_name)
    book = Book(None, repo_name=repo_name)
    book.clone_from_github()
    book.parse_book_metadata()
    result = book.add_covers() # None if there was already a cover
    if result:
        book.local_repo.commit(result)

def config_travis(repo_name, tag=False):
    repo_name = get_repo_name(repo_name)
    book = Book(None, repo_name=repo_name)
    book.clone_from_github()
    book.parse_book_metadata()
    filemaker = NewFilesHandler(book)
    filemaker.travis_files()
    book.local_repo.commit('Configure travis files')