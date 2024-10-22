#!/bin/bash

# Example commands 

globus search index list
globus search index show $INDEX_ID
globus search index show $INDEX_ID -F json
globus search query $INDEX_ID -q \*
globus search query $INDEX_ID -q \* -F json
globus search subject show $INDEX_ID "urn:ogf.org:glue2:access-ci.org:resource:cider:infrastructure.organizations:898:localid_456" 
globus search query $INDEX_ID -q 'Provider_ID:"urn:ogf.org:glue2:access-ci.org:resource:cider:infrastructure.organizations:PEARC24"'
