import { Player as TPlayer } from "../api/player/Player";

export const PLAYER_TITLE_FIELD = "id";

export const PlayerTitle = (record: TPlayer): string => {
  return record.id?.toString() || String(record.id);
};
