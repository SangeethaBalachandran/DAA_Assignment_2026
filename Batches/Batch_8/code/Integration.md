# Frontend–Backend Integration
## Industrial IoT Telemetry Compression & Network Optimization Dashboard

### 1. Overview

This document describes the integration of the frontend and backend components of the Industrial IoT Telemetry Compression & Network Optimization Dashboard developed for Batch 8 – IoT / Embedded Systems.

The application follows a client-server architecture in which the frontend handles user interaction, visualization, and dashboard management, while the backend executes compression algorithms, mathematical computations, and network telemetry simulation.

The two components communicate through REST APIs and WebSocket connections.

### 2. Integration Architecture

The application consists of three primary layers:

**Frontend Layer**
- React.js
- TypeScript
- Tailwind CSS
- React Flow
- Recharts

**Backend Layer**
- Python
- FastAPI
- Pydantic
- Huffman Coding Engine
- Shannon-Fano Algorithm
- Two-Queue Algorithm
- Package-Merge Algorithm

**Communication Layer**
- REST APIs for algorithm execution and data exchange.
- WebSockets for real-time telemetry updates.
- JSON for structured communication.

### 3. Frontend–Backend Communication

The frontend sends user inputs to the backend through HTTP requests.

The backend processes the requests, executes the required algorithms, performs mathematical calculations, and returns structured JSON responses.

The frontend uses these responses to update the dashboard, generate visualizations, and display calculated results.

The backend serves as the central source of truth for all algorithmic computations.

### 4. API Integration

The following endpoints are used for communication between the frontend and backend.

| HTTP Method | API Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check backend availability |
| POST | `/api/huffman/generate` | Generate Huffman tree and codebook |
| POST | `/api/shannon-fano/generate` | Generate Shannon-Fano codes |
| POST | `/api/huffman/two-queue` | Execute Two-Queue Huffman |
| POST | `/api/package-merge/generate` | Generate length-limited codes |
| POST | `/api/algorithms/compare` | Compare compression algorithms |
| POST | `/api/encoder/encode` | Encode sensor messages |
| POST | `/api/encoder/decode` | Decode compressed messages |
| POST | `/api/telemetry/configure` | Configure network simulation |
| POST | `/api/codebook/broadcast` | Simulate codebook broadcasting |

*Note: These are the planned integration endpoint contracts. The final endpoint list should match the implemented backend.*

### 5. WebSocket Integration

WebSockets are used to establish continuous communication between the backend telemetry simulator and the frontend dashboard.

**WebSocket endpoint:**

`/ws/telemetry`

The backend continuously generates simulated sensor telemetry and sends updated network statistics to the frontend.

The frontend receives these updates and dynamically refreshes:

- Total messages transmitted.
- Original data transmission rate.
- Compressed data transmission rate.
- Network bandwidth utilization.
- Bandwidth saved.
- Cumulative transmission statistics.
- Network status.

This enables real-time monitoring without repeatedly requesting the complete telemetry state through REST APIs.

### 6. Shared Data Flow

All four application modules use a common frequency distribution.

The default sensor status distribution is:

| Symbol | Frequency | Probability |
|---|---:|---:|
| OK | 52 | 0.52 |
| TEMP_HI | 14 | 0.14 |
| TEMP_LO | 11 | 0.11 |
| HUM | 9 | 0.09 |
| VIB | 7 | 0.07 |
| DOOR | 4 | 0.04 |
| FAULT | 2 | 0.02 |
| RESET | 1 | 0.01 |

The shared distribution ensures consistency across the Huffman Engine, Algorithm Laboratory, Network Simulator, and Hardware Constraint Inspector.

When users modify the input frequencies, the frontend sends the updated distribution to the backend for recalculation.

### 7. Module Integration

**Module 1 – Huffman Tree and Codebook Engine**

The frontend sends symbol frequencies to the Huffman API. The backend generates the optimal prefix-free codebook and returns the tree structure, binary codes, average code length, and compression statistics.

React Flow uses the returned tree data to render the interactive visualization.

**Module 2 – Algorithm Laboratory**

The frontend requests algorithm execution and comparison results from the backend.

The backend executes Huffman, Shannon-Fano, and Two-Queue algorithms and returns their respective codebooks, weighted average code lengths, and benchmark information.

The frontend displays the results through comparison tables and tree visualizations.

**Module 3 – Live Telemetry and Network Dashboard**

The frontend configures the telemetry simulation through the REST API.

The backend generates sensor messages according to the configured probability distribution and transmits updated statistics through WebSockets.

The frontend displays live network metrics and throughput charts.

**Module 4 – Embedded Hardware Constraint Inspector**

The frontend sends the symbol frequencies and maximum permitted code length to the Package-Merge API.

The backend generates a length-limited codebook and returns the resulting code lengths, average bits per message, and firmware compatibility information.

The frontend displays the constrained codebook and compares it with ordinary Huffman coding.

### 8. Local Development Configuration

The frontend and backend run independently during development.

**Backend configuration**

Default backend address:

`http://localhost:8000`

Start the backend:

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend configuration**

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws/telemetry
```

Install dependencies and start the frontend:

```bash
cd frontend

npm install

npm run dev
```

Default frontend address:

`http://localhost:5173`

**API documentation:**

`http://localhost:8000/docs`

### 9. CORS Configuration

The backend must allow requests from the frontend development server.

FastAPI CORS middleware should be configured with the frontend origin:

`http://localhost:5173`

Only the required frontend origins and HTTP methods should be allowed.

### 10. Integration Validation

The following integration tests should be performed:

| Test Case | Expected Result |
|---|---|
| Backend health check | Frontend successfully connects to backend |
| Huffman API request | Valid codebook and tree data returned |
| Shannon-Fano API request | Valid prefix-free codes returned |
| Two-Queue execution | Same optimal weighted path length as standard Huffman |
| Package-Merge execution | All code lengths satisfy the configured limit |
| Shared frequency update | All dependent modules use updated frequencies |
| WebSocket connection | Live telemetry updates received |
| Encoder and decoder | Original messages reconstructed correctly |
| Codebook broadcast | Receiver synchronization status updated |
| Invalid API input | Appropriate validation error returned |

### 11. Integration Considerations

- The backend is responsible for all algorithmic and mathematical calculations.
- The frontend must not independently calculate or hardcode compression results.
- REST API responses must follow consistent JSON schemas.
- WebSocket connections must handle disconnections and reconnections.
- All modules must use the same configured frequency distribution.
- The frontend must distinguish theoretical metrics from simulated telemetry measurements.
- Codebook versions must be synchronized between the gateway and simulated receivers.
- Communication overhead should be reported separately from theoretical compression savings.

### 12. Conclusion

The frontend–backend integration combines the interactive visualization capabilities of React with the algorithmic processing capabilities of Python FastAPI.

REST APIs provide structured communication for compression algorithms and mathematical calculations, while WebSockets support continuous telemetry updates.

This integrated architecture enables the application to demonstrate Huffman Coding, Shannon-Fano Coding, Two-Queue optimization, bandwidth analysis, and length-limited Package-Merge coding through a unified Industrial IoT simulation platform.
