
export function add(numbers: string): number {
    if (numbers === "") return 0;
    return numbers
      .split(/[\n,]/) 
      .map(Number)
      .filter(n => !isNaN(n))
      .reduce((sum, num) => sum + num, 0);
  }
  

  