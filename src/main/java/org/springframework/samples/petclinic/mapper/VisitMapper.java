package org.springframework.samples.petclinic.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.springframework.samples.petclinic.model.Visit;
import org.springframework.samples.petclinic.rest.dto.VisitDto;
import org.springframework.samples.petclinic.rest.dto.VisitFieldsDto;

import java.util.Collection;

/**
 * Map Visit & VisitDto using mapstruct
 */
@Mapper(uses = PetMapper.class)
public interface VisitMapper {
    @Mapping(source = "petId", target = "pet.id")
    Visit toVisit(VisitDto visitDto);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "pet", ignore = true)
    Visit toVisit(VisitFieldsDto visitFieldsDto);

    @Mapping(source = "pet.id", target = "petId")
    VisitDto toVisitDto(Visit visit);

    Collection<VisitDto> toVisitsDto(Collection<Visit> visits);


    // New mapping for VisitDetailDto to Visit
    @Mapping(source = "visitDetailId", target = "id")
    @Mapping(source = "visitDetailPetId", target = "pet.id")
    Visit toVisitFromDetail(VisitDetailDto visitDetailDto);

    // New mapping for Visit to VisitDetailDto
    @Mapping(source = "id", target = "visitDetailId")
    @Mapping(source = "pet.id", target = "visitDetailPetId")
    VisitDetailDto toVisitDetailDto(Visit visit);

}
