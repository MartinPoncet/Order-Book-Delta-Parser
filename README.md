# Coding Exercise Order Book Delta

This Python script parses order book delta data and logs the state of the order book in both L2 and L3 formats. It's designed to handle order book updates in the form of deltas, which represent changes to the state of the order book over time.

## Design Choices

### Class Structure
- **Order Class**: Represents an individual order with attributes for side (buy or sell), price, size, order ID, and timestamp.
- **OrderBook Class**: Manages the order book and provides methods for applying order deltas, updating the order book state, and logging the order book state in different formats.
In the "Design Choices" section, after discussing the dictionaries used, I will add the following sentence:
- **Class Side Enumeration**: Additionally, the `Side` enum was utilized to simplify conditions throughout the codebase, leveraging its boolean nature to enhance readability and maintainability.
- **Logging**: The order book states are logged in both L2 and L3 formats. To facilitate visualization and avoid cluttering the console, the output is also saved to a separate file named `logfile.log`.
- **Data Structures**: The script employs two dictionaries, one for bids and one for offers, which utilize price as keys and lists of orders as values. This design choice allows for efficient order lookup and manipulation, as the dictionaries provide constant-time complexity (O(1)) due to their hash table implementation. This ensures quick retrieval and modification of orders, contributing to the overall efficiency of the order book management system.

### OrderBook Class Methods

### `__init__()`
- **Description**: Initializes the attributes of the order book.
- **Attributes**:
  - `bids`: defaultdict to store buy side orders.
  - `offers`: defaultdict to store sell side orders.
  - `order_ids`: Dictionary to track order IDs and corresponding prices.

### `apply_delta(order)`
- **Description**: Determines the type of order event (addition, deletion, or update) and applies the corresponding operation to the order book.
- **Parameters**:
  - `order`: Order object representing the delta update.
- **Actions**:
  - Adds, deletes, or updates orders in the order book based on the delta information.

### `_add_order(order)`
- **Description**: Adds an order to the order book.
- **Parameters**:
  - `order`: Order object to be added to the order book.
- **Actions**:
  - Appends the order to the bids or offers defaultdict based on the order side.
  - Updates the `order_ids` dictionary with the order ID and corresponding price.

### `_delete_order(order)`
- **Description**: Removes an order from the order book.
- **Parameters**:
  - `order`: Order object to be removed from the order book.
- **Actions**:
  - Deletes the order from the bids or offers defaultdict based on the order side.
  - Removes the order ID and corresponding price from the `order_ids` dictionary.

### `_update_order(order)`
- **Description**: Updates an existing order in the order book.
- **Parameters**:
  - `order`: Order object representing the updated order.
- **Actions**:
  - Deletes the existing order from the order book.
  - Adds the updated order to the order book.

### `best_bid()`
- **Description**: Returns the best bid price in the order book.
- **Returns**:
  - `float`: Best bid price, or 0 if no bids exist.

### `best_ask()`
- **Description**: Returns the best ask price in the order book.
- **Returns**:
  - `float`: Best ask price, or infinity if no asks exist.

### `spread()`
- **Description**: Calculates the spread between the best bid and best ask prices. (unused here but could be useful)
- **Returns**:
  - `float`: Spread value.

### Data Structures
- **DefaultDict**: Used to store orders in the order book, with prices as keys and lists of orders as values. This allows for efficient lookup and insertion of orders by price.
- **Dictionary (order_ids)**: Maps order IDs to their corresponding prices in the order book, facilitating efficient deletion and updating of orders.

### Logging
- **L2 Format**: Logs the total size of orders at each price level for both the buy and sell sides of the order book.
- **L3 Format**: Logs individual orders with their respective prices, sides, sizes, and order IDs.

## Challenges Faced

### Delta Parsing
- **Limited Familiarity with Order Book Deltas**: While familiar with order books, handling order book deltas was a new challenge. Deltas represent changes to the order book state rather than complete snapshots, requiring careful parsing and application of updates.

### Understanding Delta Updates
- **Distinguishing Last Snapshot from Updates**: Differentiating between the last snapshot of the order book and the incoming deltas for a given price was crucial. Understanding how to interpret and apply delta updates accurately was essential to maintain the integrity of the order book.

### Absence of Initial Quantities
- **Missing Initial Quantity Information**: The data did not provide initial quantities for orders, complicating the reconstruction of the order book state. This required inferring order sizes solely from the delta updates received.

### Familiarity with Order Books
- **Understanding Order Book Structure**: While knowledgeable about order books, working with deltas highlighted nuances in order book management and maintenance. This included managing bid and ask sides, tracking order IDs, and ensuring efficient order book updates.

### Transition from L2 to L3 State Logging
- **Introduction to L3 Order Book State**: Prior experience with L2 order book state logging was helpful, but transitioning to L3 logging required additional understanding and research. This involved exploring definitions and modifications of L3 state representation to capture more granular order details.

### Delta Parsing
- Dealing with order book deltas instead of complete snapshots required implementing logic to determine whether to add, update, or delete orders based on incoming deltas.

### Negative Prices
- The presence of negative prices in the data initially seemed unusual. However, it was determined that prices and quantities were reversed in the data. However, it was assumed that the prompt referred to prices rather than quantities in this phrase: "You can recognize a 'delete' event based on the quantity (qty) field of an order when it is set to 0." Consequently, the code was adjusted to handle this inversion correctly.

### Large Data Sets
- Processing large data sets required optimizations such as splitting files and processing data incrementally to avoid memory issues.

## Running the Code

1. Ensure Python and required libraries (requirements.txt) are installed.
2. Place the input data file (e.g., `sample-data.csv.gz`) in the same directory as the script.
3. Run the script.
4. Check the generated `logfile.log` for the logged order book state in both L2 and L3 formats.