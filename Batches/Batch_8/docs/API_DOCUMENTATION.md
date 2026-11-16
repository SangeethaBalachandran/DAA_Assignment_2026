# REST API & WebSocket Documentation
## Industrial IoT Telemetry Compression & Optimization Platform

- **Base URL:** `http://localhost:8000`
- **WebSocket URL:** `ws://localhost:8000/ws/telemetry`
- **Interactive OpenAPI Docs:** `http://localhost:8000/docs`

---

## 1. System Health

### `GET /api/health`
Performs an operational health check on the gateway service.

**Response `200 OK`:**
```json
{
  "status": "healthy",
  "service": "Industrial IoT Telemetry Compression Platform",
  "version": "1.0.0",
  "network": {
    "capacity": "9.6 kbps",
    "message_rate": "40 msgs/sec",
    "sensors": 5000
  }
}
```

---

## 2. Huffman Compression Engine

### `GET /api/huffman/default`
Returns the optimal Huffman tree and codebook for the ground truth 8-symbol telemetry distribution.

**Response `200 OK`:**
```json
{
  "algorithm": "Huffman (Min-Heap)",
  "codebook": [
    {
      "symbol": "OK",
      "frequency": 52.0,
      "probability": 0.52,
      "codeword": "1",
      "length": 1,
      "register_compatible": true
    },
    {
      "symbol": "TEMP_HI",
      "frequency": 14.0,
      "probability": 0.14,
      "codeword": "010",
      "length": 3,
      "register_compatible": true
    },
    {
      "symbol": "RESET",
      "frequency": 1.0,
      "probability": 0.01,
      "codeword": "011100",
      "length": 6,
      "register_compatible": false
    }
  ],
  "codebook_map": {
    "OK": "1",
    "TEMP_HI": "010",
    "TEMP_LO": "001",
    "HUM": "000",
    "VIB": "0110",
    "DOOR": "01111",
    "FAULT": "011101",
    "RESET": "011100"
  },
  "average_length": 2.2,
  "entropy": 2.18425,
  "efficiency": 99.28,
  "redundancy": 0.01575,
  "compression_ratio": 1.3636,
  "bandwidth_savings_pct": 26.67,
  "kraft_sum": 1.0,
  "max_codeword_length": 6,
  "hardware_compatible": false,
  "operations_count": 15,
  "execution_time_ms": 0.184
}
```

### `POST /api/huffman/generate`
Constructs an optimal Huffman tree for custom symbol frequencies.

**Request Body:**
```json
{
  "frequencies": [
    { "symbol": "OK", "frequency": 52 },
    { "symbol": "TEMP_HI", "frequency": 14 },
    { "symbol": "TEMP_LO", "frequency": 11 },
    { "symbol": "HUM", "frequency": 9 },
    { "symbol": "VIB", "frequency": 7 },
    { "symbol": "DOOR", "frequency": 4 },
    { "symbol": "FAULT", "frequency": 2 },
    { "symbol": "RESET", "frequency": 1 }
  ]
}
```

---

## 3. Algorithm Laboratory Endpoints

### `POST /api/shannon-fano/generate`
Generates a Shannon-Fano codebook via top-down recursive bipartitioning.

### `POST /api/huffman/two-queue`
Executes the Two-Queue linear-time $O(N)$ Huffman algorithm (van Leeuwen, 1976), capturing all intermediate queue states.

**Response `200 OK` (Excerpt):**
```json
{
  "algorithm": "Two-Queue Huffman (O(N))",
  "average_length": 2.2,
  "operations_count": 21,
  "steps": [
    {
      "step_number": 1,
      "q1_before": ["RESET (1.0)", "FAULT (2.0)", "DOOR (4.0)", "VIB (7.0)", "HUM (9.0)", "TEMP_LO (11.0)", "TEMP_HI (14.0)", "OK (52.0)"],
      "q2_before": [],
      "popped": ["RESET:1.0 (Q1)", "FAULT:2.0 (Q1)"],
      "merged_weight": 3.0,
      "result_node": "tq_node_1 (3.0)",
      "description": "Step 1: Dequeued RESET (1.0) from Q1 and FAULT (2.0) from Q1. Enqueued new internal node tq_node_1 (3.0) into Q2."
    }
  ]
}
```

### `POST /api/package-merge/generate`
Generates an optimal length-limited prefix code with constraint $l_i \le L_{\max}$ using Package-Merge.

**Request Body:**
```json
{
  "frequencies": [
    { "symbol": "OK", "frequency": 52 },
    { "symbol": "TEMP_HI", "frequency": 14 },
    { "symbol": "TEMP_LO", "frequency": 11 },
    { "symbol": "HUM", "frequency": 9 },
    { "symbol": "VIB", "frequency": 7 },
    { "symbol": "DOOR", "frequency": 4 },
    { "symbol": "FAULT", "frequency": 2 },
    { "symbol": "RESET", "frequency": 1 }
  ],
  "max_length": 4
}
```

**Response `200 OK`:**
```json
{
  "algorithm": "Package-Merge (L<=4)",
  "average_length": 2.3,
  "kraft_sum": 1.0,
  "max_codeword_length": 4,
  "hardware_compatible": true,
  "bandwidth_savings_pct": 23.33,
  "codebook_map": {
    "OK": "0",
    "TEMP_HI": "100",
    "DOOR": "1010",
    "FAULT": "1011",
    "HUM": "1100",
    "RESET": "1101",
    "TEMP_LO": "1110",
    "VIB": "1111"
  }
}
```

### `GET /api/algorithms/counterexample?variant=8-symbol`
Returns a validated counterexample where Shannon-Fano produces strictly higher average code length than Huffman ($2.69$ vs $2.65$ bits).

### `GET /api/algorithms/benchmark`
Executes real empirical timing benchmarks across alphabet sizes $N = 8, 32, 128, 512, 1024$.

---

## 4. Message Encoder & Decoder

### `POST /api/encoder/encode`
Encodes an array of telemetry messages into a compressed bitstream.

**Request Body:**
```json
{
  "messages": ["OK", "TEMP_HI", "OK", "FAULT"],
  "algorithm": "package_merge"
}
```

**Response `200 OK`:**
```json
{
  "encoded_bitstream": "010001011",
  "message_count": 4,
  "original_bits": 12,
  "compressed_bits": 9,
  "compression_ratio": 1.3333,
  "bandwidth_saved_pct": 25.0
}
```

### `POST /api/encoder/decode`
Decodes a compressed binary bitstream back into original symbols.

**Request Body:**
```json
{
  "bitstream": "010001011",
  "codebook_map": {
    "OK": "0",
    "TEMP_HI": "100",
    "FAULT": "1011"
  },
  "codebook_version": "v1.0.0"
}
```

**Response `200 OK`:**
```json
{
  "decoded_symbols": ["OK", "TEMP_HI", "OK", "FAULT"],
  "success": true,
  "symbols_decoded": 4,
  "total_bits_consumed": 9
}
```

---

## 5. Live Telemetry & Simulation

### `GET /api/telemetry/metrics`
Returns theoretical network capacity, utilization, and bandwidth metrics.

### `POST /api/telemetry/configure`
Updates aggregate message rate, channel capacity, or sensor population.

### `POST /api/telemetry/start` | `/pause` | `/resume` | `/reset`
Controls the live telemetry simulation.

### `GET /api/telemetry/one-hour`
Calculates exact mathematical projection of transmitting 144,000 messages (1 hour) across legacy, Huffman, and Package-Merge.

---

## 6. Codebook Management

### `GET /api/codebook/current`
Returns active codebook version and mapping table.

### `POST /api/codebook/broadcast`
Simulates broadcasting an updated codebook to 5,000 receivers with ACK receipts and latency tracking.

---

## 7. Real-Time WebSocket Channel

### `WebSocket /ws/telemetry`
Streams real-time packets and metrics every 250 ms.

**Incoming Payload Format:**
```json
{
  "type": "TELEMETRY_UPDATE",
  "packets": [
    {
      "timestamp": 1740920400.12,
      "sequence_id": 142,
      "sensor_id": 3482,
      "symbol": "OK",
      "original_bits": 3,
      "codeword": "0",
      "compressed_bits": 1,
      "channel_load_bps": 40.0,
      "utilization_pct": 0.42
    }
  ],
  "status": {
    "is_running": true,
    "messages_transmitted": 142,
    "cumulative_bits_saved": 284,
    "current_bitrate_bps": 92.0
  },
  "metrics": {
    "original_bitrate": 120.0,
    "compressed_bitrate": 92.0,
    "bandwidth_saved_bps": 28.0
  }
}
```

