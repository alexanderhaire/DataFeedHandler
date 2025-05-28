# Market-Data Feed Handler

A high-performance system for ingesting, parsing, and forwarding market-data feeds (e.g., FIX/TCP, binary UDP multicast) with microsecond latency. Splits functionality into two tiers:

* **Data Plane (Rust)**: Raw network I/O, protocol parsing, batching, forwarding.
* **Control Plane (Go)**: Configuration management, dynamic subscriptions, health checks, metrics.

---

## Features

* Ultra-low latency I/O with busy-poll and core pinning
* Batch packet handling (via `recvmmsg`/`sendmmsg`)
* Dynamic subscription management over gRPC
* Prometheus-compatible metrics export
* Modular architecture for easy extension (new feed types, routers)

---

## Repository Layout

```
market_data_handler/
├── README.md                # This file
├── proto/                   # Shared protobuf definitions
│   └── control.proto
├── control_plane/           # Go-based control service
│   ├── cmd/main.go          # Entry point (HTTP & gRPC)
│   ├── api/                 # Protobuf-generated Go code
│   ├── config/              # Config structs & YAML loader
│   └── pkg/
│       ├── server/          # HTTP & gRPC handlers
│       └── metrics/         # Prometheus exporters
└── data_plane/              # Rust-based data path
    ├── Cargo.toml           # Dependencies & metadata
    ├── build.rs             # Build scripts (if needed)
    └── src/
        ├── main.rs          # Tokio runtime & bootstrap
        ├── network.rs       # Socket setup & tuning
        ├── parser.rs        # Feed protocol parsing
        └── router.rs        # Message dispatch logic
```

---

## Prerequisites

* **Rust** (1.65+), with `cargo` and `rustc`
* **Go** (1.18+), with `go` toolchain
* **protoc** (Protocol Buffer compiler)
* Linux system with support for `SO_BUSY_POLL` and `SO_REUSEPORT`

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/market_data_handler.git
cd market_data_handler
```

### 2. Generate protobuf bindings

```bash
# From repo root
protoc --go_out=control_plane/api --go-grpc_out=control_plane/api proto/control.proto
protoc --rust_out=data_plane/src proto/control.proto  # or use protobuf build.rs
```

### 3. Build & run Control Plane (Go)

```bash
cd control_plane
go build -o control-server ./cmd
./control-server --config ../config.yaml
```

### 4. Build & run Data Plane (Rust)

```bash
cd data_plane
cargo build --release
# Pin threads & start workers
./target/release/data_plane_worker --ctrl-endpoint=127.0.0.1:50051
```

---

## Configuration

Adjust `config.yaml` to define feed endpoints, routing rules, and metrics settings. Example:

```yaml
control:
  grpc_address: "0.0.0.0:50051"
data_plane:
  feeds:
    - name: "market_udp"
      protocol: "udp"
      address: "239.0.0.1:5000"
metrics:
  prometheus:
    listen_address: "0.0.0.0:9090"
```

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Commit your changes (`git commit -m "Add feature X"`)
4. Push to your branch (`git push origin feat/your-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the **Apache-2.0** License. See [LICENSE](LICENSE) for details.
