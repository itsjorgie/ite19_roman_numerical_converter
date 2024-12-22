import tkinter as tk
from tkinter import messagebox
import re

# This function validates the input characters
def valid_input(expression):
    valid_sym = {'I', 'V', 'X', 'L', 'C', 'D', 'M', '+', '-', '*', '/'}

    for char in expression:
        if char not in valid_sym:
            return False, char
    return True, None

# This function converts Roman numerals-decimal
def romanDec(roman):
    romanVal = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    total = 0
    prev_value = 0

    for char in roman:
        value = romanVal[char]
        if value > prev_value:
            total += value - 2 * prev_value  # Subtract the previous value twice
        else:
            total += value # Add the current value
        prev_value = value

    return total

# This function evaluates the Roman numeral arithmetic expression
def evaluate_expression(expression):
    # Add spaces between the Roman numerals and operators so we can split easily
    expression = re.sub(r'([IVXLCDM]+)([+\-*/])', r'\1 \2 ', expression)
    expression = re.sub(r'([+\-*/])([IVXLCDM]+)', r' \1 \2', expression)
    
    # Now split the expression into tokens (e.g., "X + V" -> ["X", "+", "V"])
    tokens = expression.split()

    # Convert Roman numerals to decimal, evaluate the arithmetic expression
    decValues = []
    for token in tokens:
        if token in '+-*/':  # Keep the operators as they are
            decValues.append(token)
        else:  # Otherwise, convert the Roman numeral to decimal
            decValues.append(str(romanDec(token)))

    # Join tokens and evaluate the expression
    try:
        result = eval(''.join(decValues))
        return result
    except Exception as e:
        messagebox.showerror("Error", "Invalid arithmetic expression.")
        return None

# Convert decimal number to words
def numberToWords(num):
    if num == 0:
        return "Zero"

    # Handle non-integer values (round to the nearest integer)
    num = round(num)  # Round the number to the nearest integer

    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", 
             "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    thousands = ["", "Thousand", "Million", "Billion", "Trillion"]

    def twoDigits(n):
        if n < 10:
            return ones[n]
        if n < 20:
            return teens[n - 10]
        return tens[n // 10] + (" " + ones[n % 10] if n % 10 else "")

    def threeDigits(n):
        if n == 0:
            return ""
        hundred = n // 100
        rest = n % 100
        result = ""
        if hundred:
            result += ones[hundred] + " Hundred"
            if rest:
                result += " " + twoDigits(rest)
        else:
            result += twoDigits(rest)
        return result

    result = ""
    group = 0
    while num > 0:
        if num % 1000 != 0:
            result = threeDigits(num % 1000) + " " + thousands[group] + " " + result
        num //= 1000
        group += 1

    return result.strip()

# Event handler for the Convert button
def convert():
    expression = romanInput.get().upper()
    if not expression:
        messagebox.showwarning("Warning", "Please enter a Roman numeral or expression.")
        return

    valid, invalid_char = valid_input(expression)
    if not valid:
        messagebox.showerror("Error", f"Invalid character: {invalid_char}")
        return

    result = evaluate_expression(expression)
    if result is not None:
        words = numberToWords(abs(result))  # Use absolute value for words
        
        # Remove negative sign from the result
        decOutput.set(f"Result: {abs(result)}")
        wordOutput.set(f"In Words: {words}")

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Providing Roman Numeral Converter")

# Configure main window size and center alignment
root.geometry("500x200")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a frame to center all widgets
frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")
frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
frame.grid_columnconfigure((0, 1), weight=1)

# Set font style and size
font_style = ("Arial", 12)

# Roman numeral input on the same line
tk.Label(frame, text="Enter Roman Expression:", font=font_style).grid(row=0, column=0, padx=10, pady=5, sticky="e")
romanInput = tk.Entry(frame, width=30, font=font_style)
romanInput.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Convert button with blue background
convertBtn = tk.Button(frame, text="Convert", width=12, font=font_style, fg="white", bg="blue", command=convert)
convertBtn.grid(row=1, column=0, columnspan=2, pady=5)

# Output labels
decOutput = tk.StringVar()
wordOutput = tk.StringVar()
tk.Label(frame, textvariable=decOutput, font=font_style).grid(row=2, column=0, columnspan=2, pady=5)
tk.Label(frame, textvariable=wordOutput, font=font_style).grid(row=3, column=0, columnspan=2, pady=5)

# Run the Tkinter event loop
root.mainloop()

#python file.py