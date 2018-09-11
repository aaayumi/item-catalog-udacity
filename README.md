# Item Catalog Project 
This is the simple application with catalog functionality. 
You can see recipes depends on categories and add/edit/delete them after login the application.

## How to use
1. Install [Vagrant]() and [VirtuallBox]()
2. Clone this repository.
3. Launch the Vagrant Virtuall Machine by running `varant up`
4. Run `vagrant ssh`
5. Switch a folder with a command `cd /vagrant`
6. Run DB with a command `python category_list.py`
7. Raunch the application with a command `python webserver.py`
8. Open it in your browser `localhost:5000`

## JSON endpoint

1. `/categories/<category_id>/JSON` returns all recipes in a specific category.


```
{
  "Recipe": [
    {
      "description": "Red curry is a popular Thai dish consisting of red curry paste cooked in coconut milk with meat added, such as chicken, beef, pork, duck or shrimp, or vegetarian protein source such as tofu.", 
      "id": 1, 
      "name": "Red Curry"
    }, 
    {
      "description": "The sauce is usually creamy and orange-coloured.", 
      "id": 2, 
      "name": "Chicken tikka masala"
    }, 
    {
      "description": "curry with chickin", 
      "id": 3, 
      "name": "Chickin curry"
    }
  ]
  ```
  2. `categories/<category_id>/<recipe_id>/JSON` returns a specific recipe in a specific category.
  
 ```
 {
  "Recipe": {
    "description": "Red curry is a popular Thai dish consisting of red curry paste cooked in coconut milk with meat added, such as chicken, beef, pork, duck or shrimp, or vegetarian protein source such as tofu.", 
    "id": 1, 
    "name": "Red Curry"
  }
}
```
  
