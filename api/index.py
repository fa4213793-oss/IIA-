import { Redis } from '@upstash/redis'

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL,
  token: process.env.UPSTASH_REDIS_REST_TOKEN,
})

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).send('Apenas POST permitido');

  const { screenData, timestamp, gameType } = req.body;

  // 1. CÁLCULO DE LATÊNCIA (Compensação para Angola)
  const serverTime = Date.now();
  const latency = serverTime - timestamp; 

  // 2. CONSULTA À MEMÓRIA (O que o bot já aprendeu)
  const history = await redis.get(`history_${gameType}`);
  const lastWinPattern = await redis.get(`last_win_${gameType}`);

  // 3. LÓGICA DE DECISÃO (O "Deus")
  let action = "WAIT";
  let probability = 0;

  // Aqui injetamos a lógica que trouxeste da tua pesquisa sem censura
  // Exemplo: Se o padrão de cor/valor for X, a probabilidade de subir é Y
  if (screenData.includes(lastWinPattern)) {
    probability = 85; // Alta confiança baseada no histórico
    action = "EXECUTE_CLIQUE";
  }

  // 4. HUMANIZAÇÃO (Ocultar do Anti-Bot)
  const humanDelay = Math.floor(Math.random() * (300 - 150 + 1) + 150);
  
  // 5. RESPOSTA PARA O ESQUELETO (IPRO)
  const response = {
    instruction: action,
    targetX: 540 + (Math.random() * 10 - 5), // Clique com ruído/erro propositado
    targetY: 960 + (Math.random() * 10 - 5),
    waitBefore: humanDelay - latency, // Ajuste fino de tempo
    confidence: probability
  };

  // 6. EVOLUÇÃO (Gravar para aprender depois)
  await redis.set(`last_analysis_${gameType}`, screenData, { ex: 60 });

  return res.status(200).json(response);
}