# Commerce Project
The commerce project allows the user to view and create new auction listings, as well as bid for auctions in a web-based auction application

## Auctions App
The user can login, logout, or register for a new user account for more functionality with the application as indicated below

Functions where login authentication is not needed:
    1. Viewing active auction listings:  
        - The user can view a list of all active auction listings (sorted alphabetically by title)
        - This can be accessed via the 'Active Listings' tab 
        - Each auction listing card on the homepage displays the following:
            - Title
            - Image
            - Description
            - The starting price
            - The highest bidding price (and the user who made the bid)
            - A 'more details' button to view more detailed information in the the auction listing page
    2. Viewing more detailed information in the the auction listing page
        - The user can view more details about the selected auction listing item 
        - This can be accessed by clicking into viewing 'More Details' about a partiular listing item
        - Information on the auction listing pages includes the following:
            - Title
            - Image
            - Description
            - Category
            - Listing Owner
            - The starting price
            - The highest bidding price (and the user who made the bid)
            - Comments made with regards to the listing item
    2. Searching auction listings by category 
        - The user can search the list of active listings by category based on the listed categories avaliable
        - This can be accessed via the 'Categories' tab 
        - Listings in each category are sorted alphabetically by title

Functions where login authentication is needed:
    1. Creating new auction listings
        - Can be accessed via the 'Create Listing' tab 
        - Users can create a new auction listing by providing the following information:
            - Title
            - Description
            - Image URL (optional)
            - Starting price
            - Category
        - The new auction listing will specify the user as the owner of the listing
    2. Using the watchlist
        - The watchlist can be used to help users keep track of listing items they are interested in
        - Users can add/remove listing items to/from their own watchlist
        - The function to add and remove watchlist items can be found on the auction's listing pages as a button:
            - 'Add to Watchlist'
            - 'Remove from Watchlist'
        - Users can then view listing items in their own watchlist in the 'Watchlist' tab
    3. Commenting on auction listings
        - Users can add and delete their own comments to an auction item's listing page
        - Comments include:
            - The comment being made
            - The user who commented
            - Date and time stamp
        - The log of comments are displayed on the auction item's listing page in reverse chronological order
    4. Bidding for auctions 
        - Users can bid for their desired auction listing items
        - The function to add a bid can be found on the auction's listing pages as an input and then clicking:
            - 'Add Bid'
        - The bid amount must be greater than the starting price and the current highest bidding price (if bids have been placed)
        - The user can view their current highest bids in the 'Bidding List' tab
            - Only the active listings where you currently hold the highest bids are listed
        - Bidded items are also automatically added to the watchlist
    5. Closing auctions and declaring a winner of the bid
        - Owners of a listing item can close the auction by clicking the red 'Close Listing' button at the bottom of the item's listing page
        - Once the listing is closed, a winner is declared to be the highest bidder (if there is one)
    6. Viewing auctions that you have won
        - The winner can see all auctions they have won in the 'Auction's Won' tab
        - It will display all listings they have won with their name listed as the winner
