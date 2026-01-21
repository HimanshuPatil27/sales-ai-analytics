# Sales Analytics Platform
An end-to-end AI-powered Sales Analytics platform for e-commerce businesses.

## Project Structure

```
/app/
├── backend/              # FastAPI backend service
│   ├── server.py        # Main API server
│   ├── requirements.txt # Python dependencies
│   └── .env            # Environment variables
├── frontend/            # React frontend application
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # Page components
│   │   ├── data/       # Mock data
│   │   ├── App.js      # Main app component
│   │   └── index.css   # Global styles
│   ├── package.json    # Node dependencies
│   └── tailwind.config.js # Tailwind configuration
├── design_guidelines.json # UI/UX design system
└── README.md           # This file
```

## Features (Initial Scaffold)

### Frontend Dashboard
- **Metric Cards**: Display key metrics (Revenue, Orders, Customers)
- **Charts**: Interactive visualizations using Recharts
  - Revenue trend line chart
  - Orders overview bar chart
- **Data Table**: Recent orders with status badges
- **Responsive Layout**: Collapsible sidebar, mobile-friendly

### Backend API
- **Endpoints**:
  - `GET /api/` - API health check
  - `GET /api/analytics/metrics` - Get key metrics
  - `GET /api/analytics/revenue` - Get revenue trend data
  - `GET /api/analytics/orders` - Get orders data
  - `GET /api/analytics/recent-orders` - Get recent order records

### Tech Stack
- **Frontend**: React 19, Tailwind CSS, Recharts, Framer Motion, Lucide Icons
- **Backend**: FastAPI, Python 3.x
- **Database**: MongoDB (configured, not actively used in scaffold)

## Design System

- **Theme**: Swiss Corporate (Professional, Data-Dense)
- **Colors**: Light mode with Navy/Slate palette
- **Typography**: 
  - Headings: Manrope
  - Body: Inter
  - Code: JetBrains Mono
- **Components**: Flat design, 1px borders, subtle hover effects

## Getting Started

The application is already running in the container environment:
- Frontend: http://localhost:3000
- Backend: http://localhost:8001

### Development

**Frontend** (hot reload enabled):
```bash
cd /app/frontend
yarn start
```

**Backend** (hot reload enabled):
```bash
cd /app/backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### Environment Variables

**Backend** (`/app/backend/.env`):
- `MONGO_URL`: MongoDB connection string
- `DB_NAME`: Database name
- `CORS_ORIGINS`: Allowed CORS origins

**Frontend** (`/app/frontend/.env`):
- `REACT_APP_BACKEND_URL`: Backend API URL

## Next Steps

1. **Data Integration**: Connect to real data sources
2. **AI Features**: Add AI-powered analytics and insights
3. **Advanced Visualizations**: More chart types and filters
4. **User Authentication**: Add login and user management
5. **Export Features**: PDF/Excel export capabilities
6. **Real-time Updates**: WebSocket integration for live data

## Notes

- This is the initial scaffold with mock data
- No data ingestion implemented yet
- No AI agents integrated yet
- All data is currently static for demonstration purposes
