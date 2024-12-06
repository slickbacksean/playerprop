import { PlayerWhereInput } from "./PlayerWhereInput";

export type PlayerListRelationFilter = {
  every?: PlayerWhereInput;
  some?: PlayerWhereInput;
  none?: PlayerWhereInput;
};
