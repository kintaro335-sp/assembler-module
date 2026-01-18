import { baseUrl } from './config'
import axios from 'axios'
// types
import { type MachineStateResp, type MessageCompileResp, type MessageResp } from './types/api-resps'

const conn = axios.create({
  baseURL: `${baseUrl}/lang`
});

export async function compileApi(program: string): Promise<MessageCompileResp> {
  const resp = await conn.post('/compile', program, {
    headers: {
      "Content-Type": "text/plain"
    }
  });

  return resp.data
}

export async function executeStepApi(): Promise<MessageResp> {
  const resp = await conn.post('/execute');

  return resp.data;
}

export async function nestTickApi(): Promise<MessageResp> {
  const resp = await conn.post('/next');

  return resp.data;
}

export async function getCurrentStateApi(): Promise<MachineStateResp> {
  const resp = await conn.get('/state');

  return resp.data;
}
