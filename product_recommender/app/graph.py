from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from .agents import *

class AppState(TypedDict):
    product_query: str
    is_specific: Optional[bool]
    video_data: Optional[List[dict]]
    relevant_videos: Optional[List[dict]]
    summaries: Optional[List[dict]]
    sentiment_score: Optional[float]
    recommendation: Optional[str]

def create_workflow():
    workflow = StateGraph(AppState)
    
    workflow.add_node("check_specificity", check_specificity)
    workflow.add_node("youtube_search", youtube_search)
    workflow.add_node("transcribe", transcribe_audio)
    # Add more nodes/edges as needed
    
    workflow.set_entry_point("check_specificity")
    workflow.add_edge("check_specificity", "youtube_search")
    workflow.add_edge("youtube_search", "transcribe")
    # Connect remaining nodes
    
    return workflow.compile()

graph = create_workflow()