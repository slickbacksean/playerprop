import { PlayerWhereInput } from "./PlayerWhereInput";
import { PlayerOrderByInput } from "./PlayerOrderByInput";

export type PlayerFindManyArgs = {
  where?: PlayerWhereInput;
  orderBy?: Array<PlayerOrderByInput>;
  skip?: number;
  take?: number;
};
