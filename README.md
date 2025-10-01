# Chemistry Problem Generator

This project is a comprehensive chemistry problem generator designed to help students practice a wide range of topics. It can generate problems from basic SI unit conversions and nomenclature to more complex topics like stoichiometry, thermodynamics, and quantum mechanics.

The application is accessible through two main interfaces:
1.  A Command-Line Interface (CLI) for a classic, terminal-based experience.
2.  A Flask-based web application for a more modern, user-friendly graphical interface.

## Core Components

The codebase is structured into several key files, each with a specific responsibility. The main logic is separated into generating problems, handling chemistry-specific data and functions, and presenting the problems to the user.

### `chem.py` - The Command-Line Interface (CLI)

This file is the original, terminal-based entry point for the application. It provides a text-based menu system for users to select and solve chemistry problems.

**Key Features:**

*   **Main Interaction Loop**: An infinite `while True` loop continuously prompts the user for input, allowing them to select problem types or change settings until they decide to exit.
*   **Problem Selection**:
    *   Users can enter a number corresponding to a specific problem type from a predefined list (`modeList`).
    *   Typing `random` or `r` selects a random problem from the currently active set.
    *   Typing `0` displays a table of contents with all available problem modes.
*   **Settings Menu**:
    *   Accessible by typing `settings`.
    *   Allows customization of the problem generation, including:
        *   **Molecule Frequency**: Adjusts the likelihood of different compound types (e.g., ionic, acid, binary) appearing.
        *   **Reaction Types**: Filters the types of chemical reactions for relevant problems.
        *   **Problem Scope**: Users can select specific "Units" or chapters, which filters the pool of random problems to a specific subset, making it great for targeted study.

### `chemFlask.py` - The Web Application

This file uses the Flask web framework to provide a modern, graphical user interface (GUI) for the problem generator, making it more accessible and intuitive.

**Key Features & Routes:**

*   **State Management**: The application uses global variables and helper functions (e.g., `setLastQuestion`, `getRandomChoices`) to manage the user's session state, such as the last question asked, the current pool of problems, and selected reaction types.
*   **Main Routes**:
    *   `/`: The home page. It provides a simple interface for the user to enter a problem number, request a random problem, or navigate to other pages.
    *   `/question/<num>`: The core of the application. It generates a question (either a specific one by `num` or a random one) and displays it to the user.
    *   `/answer`: After a question is viewed, this page reveals the corresponding answer.
    *   `/settings`: A user-friendly web form that allows for the same customizations as the CLI version (filtering by unit/chapter, reaction types, etc.).
    *   `/test`: A "test mode" that generates a user-defined number of questions at once, presenting them as a list for the user to solve. The answers are revealed on a separate page.
    *   `/polyatomic`: A dedicated page for practicing the names and formulas of polyatomic ions.

### `chemFuncts.py` - The Chemistry Engine

This is the heart of the application, containing the core logic, data structures, and scientific calculations needed to represent chemical entities and their interactions. It acts as a powerful backend library for both the CLI and the web application.

**Key Classes:**

*   **`element`**: Represents a single chemical element. It stores data like atomic number, symbol, and group, and contains methods for comparing periodic trends (e.g., `compareSize()`, `compareIE()`).
*   **`compound`**: A robust class that represents a chemical compound.
    *   It can parse a chemical formula (e.g., "H2O", "Ca(NO3)2") into its constituent atoms and their counts.
    *   It includes methods for calculating molar mass, percent composition, and the number of atoms.
    *   It contains the logic for determining chemical names from formulas (`getNameFromEq`) and predicting properties like solubility and polarity.
    *   It can even generate Lewis dot structures (`covalentBonds`) and determine VSEPR geometry.
*   **`reaction`**: Models a chemical reaction.
    *   It takes a list of reactants and a reaction type to generate the products.
    *   The `balanceEq()` method is a crucial feature that uses linear algebra (via `sympy`) to find the stoichiometric coefficients for the reaction.
    *   It can calculate the enthalpy of a reaction and format the entire balanced equation into a string.
*   **`solution`**, **`acid`**, **`base`**: These classes model aqueous solutions and are used for problems involving molarity, molality, colligative properties, and acid-base chemistry.

**Helper Functions:**

This file also contains numerous helper functions for:
*   Generating random compounds, elements, and reaction types (`getRandomCompound`, `randElement`, `randomRx`).
*   Handling chemical units and random value generation (`randUnit`, `randTemp`, `randPressure`).
*   Performing chemistry-specific calculations like electron configurations and quantum numbers.

