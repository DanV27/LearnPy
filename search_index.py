"""Smarter search autocomplete
The problem today: typing into the search bar does nothing until you submit. If you typed "binary tree", you don't know your site has a Binary Search Tree page until you've already paid for an AI generation.
With RAG: as the user types, do a quick retrieval over the 59 lessons and show the top 3 matches as suggestions below the input. Click one → instant nav to the canonical page. Skip the AI when there's a direct hit. Saves Claude calls and is way faster.
"""