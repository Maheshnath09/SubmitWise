try:
    print("Importing app.tasks.project_generation...")
    import app.tasks.project_generation
    print("Import successful!")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
