

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(on c g)
(ontable d)
(on e f)
(on f d)
(on g a)
(on h b)
(on i c)
(clear e)
(clear h)
(clear i)
)
(:goal
(and
(on a h)
(on b f)
(on c a)
(on f i)
(on g e)
(on i d))
)
)


