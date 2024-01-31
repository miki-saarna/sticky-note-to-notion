import sys
sys.path.append("/Users/mikitosaarna/Projects/notion/scan-photo-to-note")
from scripts.notion.getPages import GetPages
from inquirer import List, prompt

class PromptPageSelection:
  def __init__(self):
    print("Perhaps this doesn't need to be a class constructor")
    # self.promptUserToSelectNotionPage()

  def promptUserToSelectNotionPage(self, pageID = None):
    getPagesClass = GetPages()

    if pageID:
      pages = getPagesClass.getChildrenPagesFromParentID(parentPageID=pageID)
      pages.append({ "title": "Go back", "id": "goBack" })
    else:
      pages = getPagesClass.getChildrenPagesFromParentID() # gets workspace level pages

    pages.append({ "title": "Save note here", "id": "saveNoteHere" })

    pageTitles = list(map(lambda page: page['title'], pages)) # map of page titles
    
    questions = [List("Select page", message="Select a page or save note here:", choices=pageTitles)]
    answers = prompt(questions)

    selectedPageID = None

    if answers["Select page"] == "Save note here":
      selectedPageID = pageID
    elif answers["Select page"] == "Go back":
      try:
        grandparentPageID = getPagesClass.getParentIDFromChildID(pageID)
      except (KeyError, TypeError):
        grandparentPageID = None
      selectedPageID = self.promptUserToSelectNotionPage(pageID=grandparentPageID)
    else:
      foundPage = [page for page in pages if page.get("title") == answers["Select page"]][0] # get the page NOT as an array
      selectedPageID = self.promptUserToSelectNotionPage(pageID=foundPage["id"])

    return selectedPageID


if __name__ == "__main__":
  PromptPageSelection()