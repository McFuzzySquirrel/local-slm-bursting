@echo off
echo Stopping any running API servers...
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :8000') DO (
  echo Found process: %%P
  taskkill /F /PID %%P
)
echo Done.
