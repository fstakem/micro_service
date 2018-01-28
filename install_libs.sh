# Script params
path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
app_name=`basename $path`

# Get env
env=$ENV
echo "Installing libraries for: $env"

# Make sure using right virtualenv
correct_python=$path"/envs/"$app_name"_"$env"_env/bin/python"
python_path=`which python`

if [ $python_path != $correct_python ];
then
    echo "Incorrect virtual environment: $python_path"
    exit 1
fi

# Install requirements
base_file=$path/requirements/base.txt
requirements_file=$path/requirements/$env.txt
requirements_lock_file=$path/requirements/$env.lock

if [ -f $requirements_file ];
then
    echo "Loading requirements from: $base_file"
    pip install -r $base_file
    echo "Loading requirements from: $requirements_file"
    pip install -r $requirements_file 
    pip freeze > $requirements_lock_file
else
   echo "Error requirements file does not exist: $requirements_file"
   exit 1
fi
