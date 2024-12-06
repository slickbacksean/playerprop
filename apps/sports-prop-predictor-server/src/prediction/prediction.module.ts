import { Module } from "@nestjs/common";
import { PredictionModuleBase } from "./base/prediction.module.base";
import { PredictionService } from "./prediction.service";
import { PredictionController } from "./prediction.controller";
import { PredictionResolver } from "./prediction.resolver";

@Module({
  imports: [PredictionModuleBase],
  controllers: [PredictionController],
  providers: [PredictionService, PredictionResolver],
  exports: [PredictionService],
})
export class PredictionModule {}
