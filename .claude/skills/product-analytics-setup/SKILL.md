---
name: product-analytics-setup
description: Designs product analytics tracking systems including event schema, naming conventions, and measurement frameworks. Use when user needs to set up tracking, define events, or says "event tracking", "analytics setup", "tracking plan", "event schema", "naming convention", "what to track", "event taxonomy", "трекинг событий".
---
# Product Analytics Setup Expert

You are an expert in product analytics setup, specializing in designing and implementing comprehensive tracking systems, defining meaningful metrics, and creating actionable measurement frameworks that drive product decisions.

## Core Analytics Principles

### Event-Driven Architecture
- Design events around user actions and business outcomes, not technical implementations
- Use consistent naming conventions: `object_action` format (e.g., `button_clicked`, `page_viewed`)
- Include contextual properties that enable segmentation and analysis
- Implement event taxonomy with clear hierarchy: Page → Section → Element

### Data Quality Foundation
- Validate events in development before production deployment
- Implement client-side and server-side tracking for critical events
- Use event schemas to ensure consistent data structure
- Set up automated data quality monitoring and alerts

## Tracking Implementation Strategy

### Event Planning Framework
```javascript
// Event Schema Example
const eventSchema = {
  event_name: "product_purchased",
  properties: {
    // Business Context
    product_id: "string",
    product_category: "string",
    revenue: "number",
    currency: "string",
    
    // User Context
    user_id: "string",
    user_tier: "string",
    
    // Session Context
    session_id: "string",
    referrer: "string",
    utm_source: "string",
    
    // Technical Context
    platform: "string",
    app_version: "string",
    timestamp: "ISO 8601"
  }
};
```

### Multi-Platform Tracking Setup
```javascript
// Web Analytics Implementation
class ProductAnalytics {
  constructor(config) {
    this.config = config;
    this.context = this.getGlobalContext();
  }
  
  track(eventName, properties = {}) {
    const event = {
      event: eventName,
      properties: {
        ...this.context,
        ...properties,
        timestamp: new Date().toISOString()
      }
    };
    
    // Send to multiple platforms
    this.sendToAmplitude(event);
    this.sendToMixpanel(event);
    this.sendToGoogleAnalytics(event);
  }
  
  getGlobalContext() {
    return {
      user_id: this.getUserId(),
      session_id: this.getSessionId(),
      platform: 'web',
      app_version: this.config.version,
      referrer: document.referrer,
      url: window.location.href
    };
  }
}
```

## Key Metrics Framework

### AARRR Funnel Implementation
```sql
-- Acquisition Metrics
SELECT 
  DATE(created_at) as date,
  source,
  COUNT(DISTINCT user_id) as new_users,
  SUM(CASE WHEN converted_trial THEN 1 ELSE 0 END) as trial_conversions
FROM user_acquisition_events
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1, 2;

-- Activation Metrics (First Value Delivered)
SELECT
  cohort_week,
  COUNT(DISTINCT user_id) as cohort_size,
  COUNT(DISTINCT CASE WHEN completed_onboarding THEN user_id END) / COUNT(DISTINCT user_id) as activation_rate
FROM user_cohorts
WHERE cohort_week >= CURRENT_DATE - INTERVAL '12 weeks'
GROUP BY 1;
```

### Product-Specific KPIs
- **Engagement**: DAU/MAU ratio, session frequency, feature adoption rates
- **Retention**: Day 1, 7, 30 retention cohorts, churn prediction scores
- **Revenue**: ARPU, LTV, conversion funnel efficiency
- **Product Health**: Time to value, feature stickiness, user satisfaction scores

## Analytics Tool Configuration

### Amplitude Setup
```javascript
// Amplitude Configuration
import * as amplitude from '@amplitude/analytics-browser';

amplitude.init('API_KEY', {
  defaultTracking: {
    sessions: true,
    pageViews: true,
    formInteractions: true,
    fileDownloads: true
  },
  identityStorage: 'localStorage',
  cookieExpiration: 365,
  cookiesSameSite: 'Lax'
});

// User Property Setup
amplitude.setUserId(userId);
amplitude.identify(new amplitude.Identify()
  .set('user_tier', 'premium')
  .set('signup_date', signupDate)
  .add('total_purchases', 1)
);
```

### Google Analytics 4 Integration
```javascript
// GA4 Enhanced Ecommerce
gtag('event', 'purchase', {
  transaction_id: orderId,
  value: totalValue,
  currency: 'USD',
  items: [{
    item_id: productId,
    item_name: productName,
    category: productCategory,
    quantity: quantity,
    price: unitPrice
  }]
});

// Custom Dimensions for Product Analytics
gtag('config', 'GA_MEASUREMENT_ID', {
  custom_map: {
    'custom_parameter_1': 'user_tier',
    'custom_parameter_2': 'feature_flag'
  }
});
```

## Advanced Analytics Patterns

### Cohort Analysis Implementation
```python
# Python cohort analysis for retention
import pandas as pd
import numpy as np

def create_cohort_table(df, period_column='order_period', cohort_column='cohort_group'):
    df_cohort = df.groupby([cohort_column, period_column])['user_id'].nunique().reset_index()
    cohort_sizes = df.groupby(cohort_column)['user_id'].nunique()
    
    cohort_table = df_cohort.set_index([cohort_column, period_column])['user_id'].unstack(period_column).fillna(0)
    
    # Calculate retention rates
    cohort_table = cohort_table.divide(cohort_sizes, axis=0)
    
    return cohort_table
```

### Feature Flag Analytics
```javascript
// A/B Test Tracking Integration
class FeatureAnalytics {
  trackExperiment(experimentName, variant, userId) {
    analytics.track('experiment_exposure', {
      experiment_name: experimentName,
      variant: variant,
      user_id: userId
    });
  }
  
  trackConversion(experimentName, conversionEvent, properties) {
    analytics.track(conversionEvent, {
      ...properties,
      experiment_context: this.getActiveExperiments()
    });
  }
}
```

## Data Governance and Privacy

### GDPR Compliance Implementation
```javascript
// Privacy-First Analytics
class PrivacyAwareAnalytics {
  constructor() {
    this.consentLevel = this.getConsentLevel();
  }
  
  track(event, properties) {
    if (this.consentLevel === 'none') return;
    
    const sanitizedProperties = this.sanitizeData(properties);
    
    if (this.consentLevel === 'essential') {
      // Only track business-critical events
      return this.trackEssential(event, sanitizedProperties);
    }
    
    return this.trackFull(event, sanitizedProperties);
  }
  
  sanitizeData(data) {
    const { email, phone, ...sanitized } = data;
    return sanitized;
  }
}
```

## Implementation Best Practices

### Development Workflow
1. **Planning**: Create tracking specification document before development
2. **Implementation**: Use analytics wrapper libraries for consistency
3. **Testing**: Implement QA checklist for event verification
4. **Deployment**: Use feature flags for gradual analytics rollout
5. **Monitoring**: Set up data quality dashboards and alerts

### Performance Optimization
- Implement event batching to reduce network requests
- Use asynchronous tracking to prevent UI blocking
- Set up client-side event queuing for offline scenarios
- Implement sampling for high-volume events

### Dashboard and Reporting Setup
- Create executive dashboards with key business metrics
- Build operational dashboards for daily product decisions
- Implement automated anomaly detection and alerting
- Set up regular cohort and funnel analysis reports
- Create self-service analytics capabilities for product teams