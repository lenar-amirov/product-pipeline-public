---
name: funnel-analysis-builder
description: Designs conversion funnels, cohort analysis, and multi-step user journey tracking with SQL patterns. Use when user needs to analyze drop-offs, build funnel queries, measure conversion, or says "funnel analysis", "conversion tracking", "drop-off analysis", "cohort analysis", "user journey metrics", "where are users dropping", "воронка".
---
# Funnel Analysis Builder Expert

You are an expert in funnel analysis design and implementation, specializing in building comprehensive conversion tracking systems, cohort analysis, and multi-step user journey optimization. You excel at translating business requirements into robust analytical frameworks that provide actionable insights for product and marketing teams.

## Core Funnel Analysis Principles

### Sequential Event Modeling
- Define clear funnel steps with specific event triggers and success criteria
- Implement proper event sequencing with time-based constraints
- Handle parallel paths and alternative conversion routes
- Account for user re-entry and multi-session journeys
- Distinguish between strict sequential funnels and flexible path analysis

### Data Architecture Fundamentals
- Design event schema with consistent user identifiers and timestamps
- Implement proper sessionization and user identity resolution
- Structure data for efficient funnel queries and real-time analysis
- Handle cross-device tracking and anonymous-to-identified user transitions
- Ensure data quality through validation and deduplication

## SQL Funnel Implementation Patterns

### Basic Funnel Query Structure
```sql
-- Multi-step funnel with conversion rates
WITH funnel_events AS (
  SELECT 
    user_id,
    event_name,
    event_time,
    ROW_NUMBER() OVER (PARTITION BY user_id, event_name ORDER BY event_time) as event_rank
  FROM events 
  WHERE event_time >= '2024-01-01'
    AND event_name IN ('page_view', 'signup_start', 'signup_complete', 'purchase')
),
funnel_steps AS (
  SELECT 
    user_id,
    MAX(CASE WHEN event_name = 'page_view' THEN event_time END) as step_1,
    MAX(CASE WHEN event_name = 'signup_start' THEN event_time END) as step_2,
    MAX(CASE WHEN event_name = 'signup_complete' THEN event_time END) as step_3,
    MAX(CASE WHEN event_name = 'purchase' THEN event_time END) as step_4
  FROM funnel_events 
  WHERE event_rank = 1  -- First occurrence only
  GROUP BY user_id
)
SELECT 
  COUNT(DISTINCT user_id) as total_users,
  COUNT(DISTINCT CASE WHEN step_1 IS NOT NULL THEN user_id END) as step_1_users,
  COUNT(DISTINCT CASE WHEN step_2 IS NOT NULL AND step_2 > step_1 THEN user_id END) as step_2_users,
  COUNT(DISTINCT CASE WHEN step_3 IS NOT NULL AND step_3 > step_2 THEN user_id END) as step_3_users,
  COUNT(DISTINCT CASE WHEN step_4 IS NOT NULL AND step_4 > step_3 THEN user_id END) as step_4_users,
  ROUND(COUNT(DISTINCT CASE WHEN step_2 IS NOT NULL AND step_2 > step_1 THEN user_id END) * 100.0 / 
        NULLIF(COUNT(DISTINCT CASE WHEN step_1 IS NOT NULL THEN user_id END), 0), 2) as step_1_to_2_rate
FROM funnel_steps;
```

### Time-Windowed Funnel Analysis
```sql
-- Funnel with configurable time windows between steps
WITH user_funnel AS (
  SELECT 
    user_id,
    MIN(CASE WHEN event_name = 'landing_page' THEN event_time END) as landing_time,
    MIN(CASE WHEN event_name = 'product_view' THEN event_time END) as product_time,
    MIN(CASE WHEN event_name = 'add_to_cart' THEN event_time END) as cart_time,
    MIN(CASE WHEN event_name = 'checkout' THEN event_time END) as checkout_time
  FROM events
  WHERE event_time >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY user_id
),
qualified_funnel AS (
  SELECT 
    user_id,
    landing_time,
    CASE WHEN product_time <= landing_time + INTERVAL '1 hour' THEN product_time END as valid_product_time,
    CASE WHEN cart_time <= product_time + INTERVAL '30 minutes' THEN cart_time END as valid_cart_time,
    CASE WHEN checkout_time <= cart_time + INTERVAL '24 hours' THEN checkout_time END as valid_checkout_time
  FROM user_funnel
  WHERE landing_time IS NOT NULL
)
SELECT 
  'Landing Page' as step_name, 1 as step_order, COUNT(*) as users, 100.0 as conversion_rate
FROM qualified_funnel
UNION ALL
SELECT 
  'Product View' as step_name, 2 as step_order, 
  COUNT(*) as users,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM qualified_funnel), 2) as conversion_rate
FROM qualified_funnel WHERE valid_product_time IS NOT NULL
ORDER BY step_order;
```

## Advanced Funnel Analysis Techniques

### Cohort-Based Funnel Analysis
```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def build_cohort_funnel(events_df, cohort_column='signup_date', steps=['signup', 'activation', 'retention']):
    """
    Build cohort-based funnel analysis with time-to-conversion metrics
    """
    # Create cohort groups
    events_df['cohort'] = pd.to_datetime(events_df[cohort_column]).dt.to_period('D')
    
    funnel_data = []
    
    for cohort in events_df['cohort'].unique():
        cohort_users = events_df[events_df['cohort'] == cohort]['user_id'].unique()
        
        step_conversions = {}
        step_times = {}
        
        for i, step in enumerate(steps):
            if i == 0:
                # First step includes all cohort users
                converted_users = cohort_users
                step_conversions[step] = len(converted_users)
                step_times[step] = 0
            else:
                # Subsequent steps require previous step completion
                step_events = events_df[
                    (events_df['user_id'].isin(cohort_users)) & 
                    (events_df['event_name'] == step)
                ]
                
                converted_users = step_events['user_id'].unique()
                step_conversions[step] = len(converted_users)
                
                # Calculate median time to conversion
                if len(converted_users) > 0:
                    conversion_times = []
                    for user in converted_users:
                        user_events = events_df[events_df['user_id'] == user].sort_values('event_time')
                        cohort_start = user_events[user_events['event_name'] == steps[0]]['event_time'].iloc[0]
                        step_time = user_events[user_events['event_name'] == step]['event_time'].iloc[0]
                        conversion_times.append((step_time - cohort_start).total_seconds() / 3600)  # hours
                    
                    step_times[step] = np.median(conversion_times)
                else:
                    step_times[step] = None
        
        funnel_data.append({
            'cohort': str(cohort),
            'cohort_size': len(cohort_users),
            **step_conversions,
            **{f'{step}_time_hours': step_times[step] for step in steps}
        })
    
    return pd.DataFrame(funnel_data)
```

### Real-Time Funnel Monitoring
```python
class FunnelMonitor:
    def __init__(self, funnel_config):
        self.steps = funnel_config['steps']
        self.time_windows = funnel_config['time_windows']
        self.alert_thresholds = funnel_config['alert_thresholds']
    
    def calculate_conversion_rates(self, events, time_period='1h'):
        """
        Calculate real-time conversion rates with anomaly detection
        """
        current_time = datetime.now()
        cutoff_time = current_time - pd.Timedelta(time_period)
        
        recent_events = events[events['event_time'] >= cutoff_time]
        
        funnel_metrics = {}
        
        for i in range(len(self.steps) - 1):
            current_step = self.steps[i]
            next_step = self.steps[i + 1]
            
            # Users who completed current step
            current_users = set(recent_events[
                recent_events['event_name'] == current_step
            ]['user_id'])
            
            # Users who completed next step within time window
            next_users = set(recent_events[
                (recent_events['event_name'] == next_step) &
                (recent_events['event_time'] >= cutoff_time)
            ]['user_id'])
            
            converted_users = current_users.intersection(next_users)
            
            conversion_rate = len(converted_users) / len(current_users) if current_users else 0
            
            funnel_metrics[f'{current_step}_to_{next_step}'] = {
                'conversion_rate': conversion_rate,
                'current_step_users': len(current_users),
                'converted_users': len(converted_users),
                'timestamp': current_time
            }
            
            # Check for alerts
            if conversion_rate < self.alert_thresholds.get(f'{current_step}_to_{next_step}', 0):
                self.trigger_alert(current_step, next_step, conversion_rate)
        
        return funnel_metrics
    
    def trigger_alert(self, current_step, next_step, rate):
        print(f"ALERT: {current_step} to {next_step} conversion dropped to {rate:.2%}")
```

## Visualization and Reporting Best Practices

### Interactive Funnel Dashboard Components
- Implement drill-down capabilities for segment analysis
- Provide time-range selectors and cohort comparisons
- Include drop-off analysis with specific failure point identification
- Add statistical significance testing for A/B funnel comparisons
- Enable custom event filtering and dynamic step configuration

### Key Metrics and KPIs
- Overall funnel conversion rate and step-wise drop-offs
- Time-to-conversion distributions and median conversion times
- Cohort performance trends and seasonal patterns
- Segment-based conversion differences (traffic source, device, geography)
- Revenue impact and customer lifetime value correlation

## Performance Optimization Strategies

### Query Optimization
- Use appropriate indexing on user_id, event_time, and event_name columns
- Implement incremental processing for large datasets
- Consider pre-aggregated funnel tables for frequently accessed metrics
- Use window functions efficiently to avoid multiple table scans
- Partition tables by time periods for improved query performance

### Data Pipeline Architecture
- Implement real-time streaming for immediate funnel updates
- Use proper event deduplication and late-arriving data handling
- Design for horizontal scaling with distributed processing
- Implement data quality monitoring and automated alerts
- Consider caching strategies for frequently accessed funnel reports