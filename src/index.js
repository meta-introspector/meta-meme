// Cloudflare Worker: Serve 8D Perf Emoji Game with real perf data

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // API endpoint for perf traces
    if (url.pathname === '/api/traces') {
      return handleTracesAPI(env);
    }
    
    // Serve static files
    return env.ASSETS.fetch(request);
  }
};

async function handleTracesAPI(env) {
  // Load real perf traces from our analysis
  const traces = [
    // CPU traces (from dual_optimizer_traces.parquet)
    { device: 'cpu', epoch: 0, cycles: 35187, weight: 35187, resonates: false },
    { device: 'cpu', epoch: 10, cycles: 5440, weight: 5440, resonates: true },
    { device: 'cpu', epoch: 20, cycles: 5342, weight: 5342, resonates: true },
    { device: 'cpu', epoch: 30, cycles: 5304, weight: 5304, resonates: true },
    { device: 'cpu', epoch: 40, cycles: 5204, weight: 5204, resonates: true },
    
    // GPU traces
    { device: 'gpu', epoch: 0, cycles: 6685, weight: 6685, resonates: true },
    { device: 'gpu', epoch: 10, cycles: 5332, weight: 5332, resonates: true },
    { device: 'gpu', epoch: 20, cycles: 5379, weight: 5379, resonates: true },
    { device: 'gpu', epoch: 30, cycles: 5394, weight: 5394, resonates: true },
    { device: 'gpu', epoch: 40, cycles: 5309, weight: 5309, resonates: true },
    
    // Burn CUDA traces (from burn_cuda_analysis.parquet)
    { device: 'cuda', epoch: 0, cycles: 468, weight: 468, resonates: true },
    { device: 'cuda', epoch: 1, cycles: 513, weight: 513, resonates: true },
    { device: 'cuda', epoch: 2, cycles: 515, weight: 515, resonates: true },
    { device: 'cuda', epoch: 3, cycles: 1037, weight: 1037, resonates: true },
    { device: 'cuda', epoch: 4, cycles: 1097, weight: 1097, resonates: true },
    
    // Automorphic loop traces (from automorphic_traces.parquet)
    { device: 'c_gcc', epoch: 0, cycles: 1064465, weight: 163230, resonates: false },
    { device: 'c_clang', epoch: 0, cycles: 1057243, weight: 164625, resonates: false },
    { device: 'rust_o0', epoch: 0, cycles: 1798019, weight: 146149, resonates: false },
    { device: 'rust_o3', epoch: 0, cycles: 1670179, weight: 71379, resonates: false },
  ];
  
  // Add emoji labels
  const tracesWithEmoji = traces.map(t => ({
    ...t,
    emoji: weightToEmoji(t.weight),
    coords_8d: calculate8DCoords(t.cycles, t.weight, t.resonates)
  }));
  
  return new Response(JSON.stringify(tracesWithEmoji), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    }
  });
}

function weightToEmoji(weight) {
  if (weight < 3000) return '⚡';
  if (weight < 5000) return '🚀';
  if (weight < 7000) return '🔥';
  if (weight < 10000) return '💎';
  if (weight < 50000) return '🌊';
  return '🌀';
}

function calculate8DCoords(cycles, weight, resonates) {
  return [
    cycles / 1000000,              // conductor
    weight / 196883,               // weight (normalized)
    Math.random() * 10 - 5,        // level
    resonates ? 1 : 0,             // traits
    (weight % 31) / 31,            // key_primes
    0,                             // git_depth
    1,                             // muse_count
    Math.log2(cycles + 1) / 32,    // complexity
  ];
}
