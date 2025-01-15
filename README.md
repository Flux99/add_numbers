# add_numbers

# String Calculator - TDD Kata

## 🛠 Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Flux99/add_numbers.git
   cd add_numbers
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

## 🚀 Running Tests
To run tests:
```sh
npm test
```

To run tests in watch mode:
```sh
npm run test:watch
```

## 🎯 Features
- Handles empty input
- Supports comma-separated numbers
- Allows newlines as separators
- Supports custom delimiters (`//;
1;2` → `3`)
- Throws an error for negative numbers (`Negative numbers not allowed: -2, -4`)

## 📝 Example Usage
```ts
import { add } from "./src/add";

console.log(add("1,2,3"));  
console.log(add("//;\n1;2")); 
console.log(add("1\n2,3")); 
console.log(add("")); 
console.log(add("1,-2,3,-4"));
```

## 📌 Test-Driven Development (TDD) Approach
This project follows the **TDD methodology**, meaning:
1. Write a failing test.
2. Implement the simplest solution to pass the test.
3. Refactor and optimize while keeping tests passing.

Happy Coding! 🚀

