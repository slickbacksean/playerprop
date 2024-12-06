import { GameWhereInput } from "./GameWhereInput";
import { GameOrderByInput } from "./GameOrderByInput";

export type GameFindManyArgs = {
  where?: GameWhereInput;
  orderBy?: Array<GameOrderByInput>;
  skip?: number;
  take?: number;
};
