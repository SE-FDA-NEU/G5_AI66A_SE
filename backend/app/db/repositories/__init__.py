"""Every query the app runs, one module per table.

The contract with the service layer (agreed on #60 and #61):
- a repository only reads and writes rows; business rules live in app/services;
- a service never writes a query of its own; it calls a function here.
"""
