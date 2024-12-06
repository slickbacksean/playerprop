import { Game as TGame } from "../api/game/Game";

export const GAME_TITLE_FIELD = "id";

export const GameTitle = (record: TGame): string => {
  return record.id?.toString() || String(record.id);
};
