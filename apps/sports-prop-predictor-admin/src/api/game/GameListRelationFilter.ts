import { GameWhereInput } from "./GameWhereInput";

export type GameListRelationFilter = {
  every?: GameWhereInput;
  some?: GameWhereInput;
  none?: GameWhereInput;
};
