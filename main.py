from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional

# Initialize FastAPI app
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        return f.read()



# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows cookies and authorization headers
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Load the CSV file into a pandas DataFrame at startup
FILE_PATH = "final_output.csv"  # Update with your actual file path
# df = pd.read_csv(FILE_PATH)
df = pd.read_csv(FILE_PATH, low_memory=False)


# Define the function

def filter_colleges_by_nearest_rank(df, data):
    try:
        district = data.districts
        category = data.category
        gender = data.gender
        scoreCompar = float(data.rank) if data.scoreType =="rank" else float(data.percentage), 
        scoreType= "r" if data.scoreType =="rank" else "p"
        print(scoreType)
        course_name = data.courseName
        college_type = data.collegeType 
        top_n= data.topN
        print(data)
        # Clean the dataframe
        df.columns = df.columns.str.strip().str.lower()
        df['district'] = df['district'].str.strip().str.lower()
        df['course name'] = df['course name'].str.strip().str.lower()
        df['college type'] = df['college type'].str.strip().str.lower()
        df = df.dropna(subset=['district', 'course name', 'college type'])

        # Ensure the rank columns are numeric
        columns_to_exclude = ['college code', 'college name', 'choice code', 'course name',
                            'district', 'college type']
        df = df.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name not in columns_to_exclude else x)

        # Filter by district
        filtered_df = df[df['district'].str.contains(district.lower(), case=False, na=False)]

        # Filter by course name
        if course_name:
            filtered_df = filtered_df[filtered_df['course name'].str.contains(course_name.lower(), case=False, na=False)]

        # Filter by college type
        if college_type:
            filtered_df = filtered_df[filtered_df['college type'].str.contains(college_type.lower(), case=False, na=False)]
        scoreCompar = scoreCompar[0]
        print(scoreCompar)

        # Ensure rank column is greater than the specified rank
        # filtered_df = filtered_df[filtered_df[f"gopen-i-{scoreType}"] > float(scoreCompar)] 
        # Handle dynamic category filtering
        category_filter = pd.DataFrame()
        fixed_columns = ['college code', 'college name', 'choice code', 'course name', 'district', 'college type']
    

        if category:
            for i in ["mi","ii","i","vii"]:
                category_column = f"{gender}{category}-{i}-{scoreType}" if category.upper() in ["OPEN", "SC", "ST", "NTA", "NTB", "NTC", "NTD", "OBC"] else f"{category}-{i}-{scoreType}"
                print(category_column)
                # if category_column in filtered_df.columns:
                    
                #     filtered_rows = filtered_df[filtered_df[category_column] > float(scoreCompar) if scoreType=="r" else filtered_df[category_column] < float(scoreCompar)]
                #     category_filter = pd.concat([category_filter, filtered_rows])
                if category_column in filtered_df.columns:
            
                    # Filter rows based on score comparison logic
                    filtered_rows = filtered_df[filtered_df[category_column] > float(scoreCompar) if scoreType == "r" else filtered_df[category_column] < float(scoreCompar)]
                    
                    # Select relevant columns: all except 'college_code', 'college_name', and the category_column (score column)
                    # other_columns = [col for col in filtered_df.columns if col not in ['college code', 'college name', category_column]]
                    
                    # # Create a new DataFrame with selected columns
                    # filtered_columns = filtered_rows[['college code', 'college name', category_column] + other_columns]
                    selected_columns = fixed_columns + [col for col in filtered_df.columns if f"{gender}{category}" in col ]
            
            # Select only the relevant columns from the filtered rows
                    filtered_columns = filtered_rows[selected_columns]
                    category_columns = [col for col in selected_columns if category in col]
                    if category_columns:
                        # Combine the values of all category columns into a single column
                        filtered_columns['category_column_combined'] = filtered_columns[category_column]
                        
                        # Drop the original category columns
                        filtered_columns.drop(columns=category_columns, inplace=True)
                    
                    # Concatenate the filtered rows into the category_filter DataFrame
                    # Concatenate the filtered rows into the category_filter DataFrame
                    category_filter = pd.concat([category_filter, filtered_columns], axis=0)
                    # Concatenate these filtered rows into the category_filter DataFrame
                    # category_filter = pd.concat([category_filter, filtered_rows], axis=0)

        # category_filter = pd.DataFrame()

        # Drop NaN columns if necessary
        # category_filter.dropna(axis=1, how='any', inplace=True)

#       Merge all columns into one single column 'all_columns'
        # category_filter['all_columns'] = category_filter.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
        print(category_filter)
        # Optionally, you can drop the individual category columns and keep only the merged column

        # category_filter.drop(columns=[col for col in category_filter.columns if col not in ['college code', 'college name', 'all_columns']], inplace=True)
        category_filter.dropna(axis=1, how='all', inplace=True)

        # category_filter.drop(columns=[col for col in category_filter.columns if col != 'all_columns'], inplace=True)
        print("asdfas",category_filter.columns.to_list())
        # If no results are found, return empty
        # if filtered_df.empty:
        #     return []
        # Sort by rank and get top_n results
        sortvalue = category_filter.sort_values(by=f'category_column_combined', ascending=True if scoreType =="r" else False)
        closest_colleges = sortvalue.head(top_n)

        print("dsf ",closest_colleges)
        # Extract college names
        return closest_colleges[['college code', 'college name',  'category_column_combined']].to_dict()
    except Exception as e : 
        print(e)
        return []

# Define request schema
# {
#     "studentName": "1",
#     "gender": "g",
#     "scoreType": "rank",
#     "rank": "1",
#     "percentage": "",
#     "category": "def-o",
#     "districts": "amravati",
#     "courseName": "computer engineering",
#     "collegeType": "un-aided"
# }
class CollegeFilterRequest(BaseModel):
    studentName:str
    scoreType: str
    gender:str
    districts: str
    category: Optional[str] = None
    rank: str
    percentage:str
    courseName: Optional[str] = None
    collegeType: Optional[str] = None
    topN: Optional[int] = 20

# Define API endpoint
@app.post("/filter-colleges/")
async def filter_colleges(request: CollegeFilterRequest):
    try:
        # Call the filtering function with user inputs
        result = filter_colleges_by_nearest_rank(
            df=df,
            data=request
        )
        # Return results
        if not result:
            return {"message": "No colleges found for the given criteria."}

        return {"colleges": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
