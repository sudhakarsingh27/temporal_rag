import matplotlib.pyplot as plt
import datetime

def plot_timeline_point(date_str, ax=None, color='blue'):
    """
    Plot a point on a timeline.
    
    Args:
        date_str (str): Date string in format 'YYYYMMDD'
        ax (matplotlib.axes.Axes, optional): Existing axes to plot on. If None, creates new axes.
        color (str): Color of the point and text
    
    Returns:
        matplotlib.axes.Axes: The axes object with the plot
    """
    # Convert date string to datetime object
    date_point = datetime.datetime.strptime(date_str, "%Y%m%d")
    
    # Create new figure and axis if none provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 2))
        
        # Set axis limits
        start_date = datetime.datetime(2000, 1, 1)
        end_date = datetime.datetime(2024, 12, 31)
        ax.set_xlim(start_date, end_date)
        ax.set_ylim(-0.5, 0.5)
        
        # Remove ticks and labels
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_xticklabels([])
        
        # Add horizontal line
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        
        # Remove the frame
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

    # Plot the point with specified color
    ax.plot(date_point, 0, 'o', color=color, markersize=10)
    
    # Add the date as text above the point with same color
    ax.annotate(date_point.strftime('%Y-%m-%d'), 
                xy=(date_point, 0),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                color=color)

    return ax

# Example usage:
if __name__ == "__main__":
    # Create initial plot
    fig, ax = plt.subplots(figsize=(10, 2))
    
    # Plot multiple points with different colors
    ax = plot_timeline_point("20220315", ax, color='blue')
    ax = plot_timeline_point("20230601", ax, color='red')
    ax = plot_timeline_point("20240101", ax, color='green')
    ax = plot_timeline_point("20210715", ax, color='purple')
    ax = plot_timeline_point("20231225", ax, color='orange')
    
    plt.show()