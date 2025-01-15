export function add(numbers: string): number {
    if (numbers === "") return 0;
  
    let delimiter = /,|\n/; 
    if (numbers.startsWith("//")) {
      const delimiterEnd = numbers.indexOf("\n");
      delimiter = new RegExp(numbers.substring(2, delimiterEnd), "g");
      numbers = numbers.substring(delimiterEnd + 1); 
    }
  
    const numArray = numbers.split(delimiter).map(Number).filter(n => !isNaN(n));
    const negatives = numArray.filter(n => n < 0);
    
    if (negatives.length > 0) {
      throw new Error(`Negative numbers not allowed: ${negatives.join(", ")}`);
    }
    
    return numArray.reduce((sum, num) => sum + num, 0);
  }
  