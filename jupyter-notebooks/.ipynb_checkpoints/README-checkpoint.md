# Jupyter Notebooks for the  HPC‐ED Metadata Project 

## Project website: https://github.com/HPC-ED/HPC-ED.github.io/wiki

## Project Description:
The HPC-ED  project team is building a platform for the community to better share and find training materials through a federated repository. This project was started when a group of HPC community members got together to discuss how difficult it was to find and share training materials.

To improve the sharing and discovery of CyberTraining materials, the HPC-ED Pilot project team is building a platform for the community to better share and find training materials through a federated catalog. The platform, currently in early test mode, is focused on a flexible platform, informative metadata, and community participation. By creating a framework for identifying, sharing, and including content broadly, HPC-ED will: allow providers of training materials to reach new groups of learners; extend the breadth and depth of training materials; and enable local sites to add or extend local portals.

## About these Notebooks
The notebooks in this collection are designed to demonstrate how to use the HPC-ED Globus-based commnand linke interface (CLI) tools to search and ingest data from the HPC-ED repository. The current set of notebooks and files include:

| **NOTEBOOKS** | **DESCRIPTION** |
| --------------| --------------| 
| hpc-ed-ingest-cli.ipynb | Upload/Ingest material using globus-cli (CLI) |
| hpc-ed-search-cli.ipynb | Search/download material using globus-cli (CLI) |
| hpc-ed-json-file-builder.ipynb | Create a JSON formatted file for ingestion into the Federated Materials Repository |
| hpc-ed-gme-generator.ipynb | Python code to create and save an HPC-ED JSON formatted file to be used for ingesting into the repository |
| input_data | folder contains input data used by the notebooks |
| output_data | folder contains output data used by the notebooks |

## To use these notebooks:
You need to update your HPC-ED Credentials. Edit the file in 
```
src/credential.sh
```

## Notebooks and bash magic
To run the ```CLI``` commands from a notebook, the simplest methods is to run ```bash``` commands. To obtain the needed functionality, we are using ```%%bash``` magic command to process python variables. 
* For more details, see: https://ipython.readthedocs.io/en/stable/interactive/magics.html
* Bash magic cheat sheet: https://www.kdnuggets.com/jupyter-notebook-magic-methods-cheat-sheet#:~:text=Magic%20methods%20are%20special%20commands,cell%20and%20start%20with%20%25%25.

 ## Future Plans
Future plans include using the ```globus-sdk``` for more advance notebook capabilities. The Globus SDK provides a convenient Pythonic interface to Globus web APIs, including the Transfer API and the Globus Auth API. For more information, see:  https://globus-sdk-python.readthedocs.io/en/stable/
