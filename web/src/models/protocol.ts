import { Audited } from "./audited";
import { BlockDefinition } from "./block-definition";

export interface Protocol extends Audited {
    id?: number;
    name?: string;

    blocks?: BlockDefinition[];
}
