\# GeoPulse Setup Guide (Windows)



\## 1. Prerequisites

\- Git

\- Java 17 (Temurin): `winget install EclipseAdoptium.Temurin.17.JDK`

\- Python 3.11: `winget install Python.Python.3.11`

\- A Snowflake account (free trial)



\## 2. Clone and create the environment

```powershell

git clone https://github.com/arju109/geopulse.git

cd geopulse

py -3.11 -m venv .venv

Set-ExecutionPolicy -Scope CurrentUser RemoteSigned   # once, if activation is blocked

.venv\\Scripts\\Activate.ps1

python -m pip install "pyspark==3.5.3" "apache-sedona==1.6.1" shapely attrs pandas numpy pytest

python -m pip install "numpy<2" "pyarrow<18"

python -m pip install "snowflake-connector-python\[pandas]" python-dotenv dbt-snowflake

```



\## 3. Hadoop on Windows (Spark needs it)

```powershell

mkdir C:\\hadoop\\bin

$base = "https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-3.3.5/bin"

Invoke-WebRequest "$base/winutils.exe" -OutFile C:\\hadoop\\bin\\winutils.exe

Invoke-WebRequest "$base/hadoop.dll" -OutFile C:\\hadoop\\bin\\hadoop.dll

setx HADOOP\_HOME "C:\\hadoop"

```

In every new terminal:

```powershell

$env:HADOOP\_HOME = "C:\\hadoop"

$env:PATH = "C:\\hadoop\\bin;" + $env:PATH

```



\## 4. Credentials

Create `.env` in the repo root (never commit it):

```

SNOWFLAKE\_ACCOUNT=ORGNAME-ACCOUNTNAME

SNOWFLAKE\_USER=your\_username

SNOWFLAKE\_PASSWORD=your\_password

SNOWFLAKE\_WAREHOUSE=GEOPULSE\_WH

SNOWFLAKE\_DATABASE=GEOPULSE

SNOWFLAKE\_SCHEMA=RAW

```

Load it into the current terminal (needed for dbt):

```powershell

Get-Content .env | ForEach-Object { if ($\_ -match '^\\s\*(\[^#=]+)=(.\*)$') { Set-Item "env:$($matches\[1].Trim())" $matches\[2].Trim() } }

```



\## 5. Run the pipeline

```powershell

python data\_generation\\generate\_pings.py 3000000 20000       # mock pings (Parquet)

python spark\_sedona\\jobs\\catchment\_audit.py 2g               # Sedona spatial audit

\# Run snowflake\\create\_tables.sql in a Snowsight worksheet, then:

python snowflake\\load\_data.py 3000000                        # load into Snowflake

cd dbt\_project

dbt run --profiles-dir .

dbt test --profiles-dir .

```



\## 6. Troubleshooting

| Error | Fix |

|---|---|

| `running scripts is disabled` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

| `No module named ...` | The venv is not active (prompt must start with `(.venv)`) |

| `Could not locate Hadoop executable ... winutils.exe` | Put `winutils.exe` and `hadoop.dll` in `C:\\hadoop\\bin`, set `HADOOP\_HOME` |

| `Illegal Parquet type: TIMESTAMP(NANOS)` | Write timestamps as microseconds (`astype("datetime64\[us]")`) |

| `pyarrow requires NumPy 2.0` | `pip install "pyarrow<18" "numpy<2"` |

| `UnsatisfiedLinkError NativeIO` | Do not write Parquet from Spark on Windows; count results, or use WSL |

| `No dbt\_project.yml found` | Wrong branch: merge the dbt branch or run dbt from `dbt\_project\\` |

| `git push` 403 | Wrong GitHub account saved in Credential Manager |

