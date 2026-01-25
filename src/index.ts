/**
 * @metameme/lattice - Pure function lattice with URL-encoded proofs
 */

export interface ProofShard {
  id: number;
  theorem: string;
  proof: string;
  hash: string;
}

export interface FunctionLattice {
  functions: Map<string, Function>;
  proofs: ProofShard[];
  properties: string[];
}

export class URLProof {
  static encode(shard: ProofShard): string {
    const data = btoa(JSON.stringify(shard));
    return `#proof/${shard.id}/${shard.hash}/${data}`;
  }

  static decode(url: string): ProofShard | null {
    const match = url.match(/#proof\/(\d+)\/([^\/]+)\/(.+)/);
    if (!match) return null;
    
    try {
      const data = JSON.parse(atob(match[3]));
      return { id: parseInt(match[1]), hash: match[2], ...data };
    } catch {
      return null;
    }
  }

  static shard(url: string, count: number): string[] {
    return Array.from({ length: count }, (_, i) => `${url}/shard/${i}`);
  }
}

export class Lattice {
  private functions = new Map<string, Function>();
  private proofs: ProofShard[] = [];

  add(name: string, fn: Function, proof: ProofShard): void {
    this.functions.set(name, fn);
    this.proofs.push(proof);
  }

  toURL(base: string): string {
    const props = Array.from(this.functions.keys()).join(';');
    const proofHashes = this.proofs.map(p => p.hash).join(',');
    return `${base}?props=${props}&proofs=${proofHashes}`;
  }

  static fromURL(url: string): Lattice {
    const lattice = new Lattice();
    const params = new URLSearchParams(url.split('?')[1]);
    // Reconstruct from URL shards
    return lattice;
  }
}

export default { URLProof, Lattice };
