# Introduction #

This is a holding page while the main ADMIRAL wiki is out of action, for a summary of the current ADMIRAL project tasks.


# Tasks #

## Current ##

  1. Browse button or tree display on submission form (try tree display first, default collapsed to top level)

## To Do ##

  1. Dataset list interface:
    * Show only the unpacked datasets in the list of datasets (How to detect? See message from Anusha about different resources types.)
    * Refactor HTTPUTILS to use an object for session pattern (suggest we review revised API proposal before starting on code).
    * Test scripts to run all tests.
  1. Databank tasks (changes to be made by Anusha ):
    * Comments on Databank dataset display interface are these done yet?)
      * "Item's Embargo state" should be "Item's embargo state" (consistent case)
      * "Item's RDF Manifest" should be "Item's RDF manifest"
      * "Change RDF Manifest" should be "Change RDF manifest"
      * "Add File to ..." should be "Add file to ..."

## Discussion needed ##

  1. Dataset list interface:
    * Option to expose directory map (tree) in submitted dataset list display?
    * By default, CH wants to see only personally submitted datasets, with an option to see all datasets submitted by his group. Suggestion that only RG leader can see all datasets (I think this may be harder to do)
    * Possibly want to see all people who have submitted any version of a dataset - need to work through access issues with library services.
  1. Need discussion on Select Datasets page :
    * If username = email address, that would work well enough?
    * Implement filters, what are they?
  1. ADMIRAL banner on web page (help to distinguish ADMIRAl displays from Databank displays)(Have emailed, but awaiting response from Sally, Anusha predicts it is Ben who created the logo)
  1. Embargo setting: default value (near term or distant future?); authorization to release; pre-authorized future releases. Needs a proposal. Ask Cambridge how they handle this.
  1. Need some clarification of roles: who can submit a dataset; who can release a dataset for publication? WHo can respond to an embargo-release prompt?  -   Databank
  1. Lots of detail in the Databank web page display should not be visible to typical ADMIRAL user. (might help to get Chris involved in meeting with Anusha?)
  1. Granularity of silo alllocation will affect what datasets are potentially visible. Favour granularity at research group level (which I think is what we've discussed with library services)
  1. Default embargo data (a) in far future, or (b) short date provided that further confirmation is required before data is released.


## Completed ##


### Prior to 2010-12-21 ###

  1. Use dataset name as given for unpacked data; add "-packed" suffix for ZIP file version
  1. Confirmation page: "back to front page" link should be clearer "return toi ADMIRAL front page"
  1. Confirmation page: option to resubmit dataset
  1. Databank view links: put these on the ADMIRAL view of the dataset, rather than on the conformation page -1
  1. Last modified (include?)
  1. "Created by" -> "Submitted by"
  1. "Last modified" -> "Submission date" and include version alongside
  1. Add confirmation page showing dataset content (like view page) before actually performing submission
  1. Also show: version number, when submitted, who submitted. Include additional metadata naming submitter (ADMIRAL username or personal name? If username = email address, that would work well enough?)
  1. Include links to library service databank entries for packed and unpacked versions
  1. Databank tasks :
    * Dataset versioning should start at 1, not 2. Suggest initial empty dataset is version 0.

### yyyy-mm-dd ###

(template: copy this to above, edit date into heading, and add completed tasks)