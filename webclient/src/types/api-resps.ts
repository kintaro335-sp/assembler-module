
interface ModuleState {
  req_input: boolean;
  acc: number;
  bak: number;
  step: number;
  instructions: Array<string[]>
}

interface MemStackState {
  mem: string[];
}

export interface MachineStateResp {
  executed: boolean;
  tick: number;
  modules: Record<string, ModuleState>;
  mem_stacks: Record<string, MemStackState>
}

export interface MessageResp {
  message: string;
}

export interface MessageCompileResp {
  message: string;
  success: boolean;
}
