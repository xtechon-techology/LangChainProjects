echo "Starting FastAPI Server"
cd /Users/vishald/Documents/DWL/langchain/LangChainProjects
echo "Changed directory to LangChainProjects"
deactivate
echo "Deactivated virtual environment"
source /Users/vishald/Documents/DWL/langchain/LangChainProjects/.venv/bin/activate
echo "Activated virtual environment"
cd fast_api_rest_server
echo "Changed directory to fast_api_rest_server"
uvicorn main:app --reload
echo "Started FastAPI Server"