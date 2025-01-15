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
    
});


