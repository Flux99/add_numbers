import { add } from "../app";

describe("String Calculator", () => {
  it("should return 0 for an empty string", () => {
    expect(add("")).toBe(0);
  });
  it("should return the sum of two numbers", () => {
    expect(add("1,5")).toBe(6);
  });
  it("should return the sum of multiple numbers", () => {
    expect(add("1,2,3,4,5")).toBe(15);
  });
  it("should handle new lines between numbers", () => {
    expect(add("1\n2,3")).toBe(6);
  });
  it("should ignore non-numeric values with custom delimiters", () => {
    expect(add("//;\n1;2;a;3")).toBe(6);
  });
  it("should support custom delimiters", () => {
    expect(add("//;\n1;2")).toBe(3);
  });
  
});


