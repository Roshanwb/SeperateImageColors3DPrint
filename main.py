import tkinter as tk
from interface import ModernColorReductionApp

def main():
    """Clean, professional application entry point"""
    root = tk.Tk()
    app = ModernColorReductionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()