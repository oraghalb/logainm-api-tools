# Logainm API Tools

A collection of example Python scripts to guide users as to how they might retrieve, parse and use data from the Logainm API ([docs.gaois.ie](https://docs.gaois.ie/en/data/getting-started)).

## Script 1: logainm_api_results_to_table.py

This script gets a list of places of a specified type from a specified county in Ireland from the Logainm API and prints place metadata (one place per line) to a TSV formatted file with the following columns:

```
logainm_id | lat | lon | county | barony | parish | cats | names_en | names_ga
```

For example, for townlands (BF) in Carlow (100004), this would be the first five lines of output (vertical bars are inserted here for clarity):

```
3000 | 52.8268601272065 | -6.58634818810364 | 100004 Carlow | 1 Rathvilly | 1411069 Clonmore | townland | Ballaghaclay | Bealach an tSléibhe  
3001 | 52.8388492391207 | -6.53371364645032 | 100004 Carlow | 1 Rathvilly | 1411069 Clonmore | townland | Ballinagilky | Baile na Giolcaí  
3002 | 52.8365069012364 | -6.60636780935882 | 100004 Carlow | 1 Rathvilly | 1411069 Clonmore | townland | Ballyduff | An Baile Dubh  
3003 | 52.8258526764742 | -6.60526952627927 | 100004 Carlow | 1 Rathvilly | 1411069 Clonmore | townland | Ballynakill | Baile na Coille  
3004 | 52.8235812668175 | -6.54264046126135 | 100004 Carlow | 1 Rathvilly | 1411069 Clonmore | townland | Bellmount | Bellmount  
...
```

This script can easily be modified to produce different output.

## Script 2: lorem ipsum

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
